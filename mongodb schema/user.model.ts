import mongoose, { Schema } from "mongoose";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import type { IUser } from "../types/user.types.js";

/**
 * Mongoose schema for User
 */
const userSchema = new Schema<IUser>(
  {
    email: {
      type: String,
      required: [true, "Email is required"],
      unique: true,
      lowercase: true,
      trim: true,
      index: true,
    },
    password_hash: {
      type: String,
      select: false, // Don't include in queries by default
    },
    name: {
      type: String,
      required: [true, "Name is required"],
      trim: true,
    },
    phone: {
      type: String,
      trim: true,
    },
    // OAuth fields
    oauth_provider: {
      type: String,
      enum: ["local", "google", "microsoft"],
      default: "local",
    },
    oauth_id: {
      type: String,
      sparse: true, // Allow null but must be unique if present
      index: true,
    },
    profile_picture: {
      type: String,
    },
    // Email verification
    email_verified: {
      type: Boolean,
      default: false,
    },
    email_verification_token: {
      type: String,
      select: false,
    },
    email_verification_expires: {
      type: Date,
      select: false,
    },
    // Password reset
    password_reset_token: {
      type: String,
      select: false,
    },
    password_reset_expires: {
      type: Date,
      select: false,
    },
    // Security
    last_login_at: {
      type: Date,
    },
    failed_login_attempts: {
      type: Number,
      default: 0,
    },
    account_locked_until: {
      type: Date,
    },
    // Refresh tokens
    refresh_tokens: {
      type: [String],
      default: [],
      select: false,
    },
    // Status
    active: {
      type: Boolean,
      default: true,
      index: true,
    },
  },
  {
    timestamps: {
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
    collection: "users",
  }
);

// Indexes for common queries
userSchema.index({ taxpayer_id: 1, active: 1 });
userSchema.index({ email: 1, active: 1 });
userSchema.index({ oauth_provider: 1, oauth_id: 1 });

// Virtual for businesses (if needed later)
userSchema.virtual("businesses", {
  ref: "Business",
  localField: "taxpayer_id",
  foreignField: "taxpayer_id",
});

// Pre-save hook to hash password
userSchema.pre("save", async function () {
  // Only hash password if it's modified and exists
  if (!this.isModified("password_hash") || !this.password_hash) {
    return;
  }

  const salt = await bcrypt.genSalt(10);
  this.password_hash = await bcrypt.hash(this.password_hash, salt);
});

// Method to compare password
userSchema.methods.comparePassword = async function (
  candidatePassword: string
): Promise<boolean> {
  if (!this.password_hash) {
    return false; // OAuth users don't have passwords
  }
  return bcrypt.compare(candidatePassword, this.password_hash);
};

// Method to handle failed login attempt
userSchema.methods.handleFailedLogin = async function (): Promise<void> {
  this.failed_login_attempts += 1;

  // Lock account after 5 failed attempts
  if (this.failed_login_attempts >= 5) {
    this.account_locked_until = new Date(Date.now() + 15 * 60 * 1000); // 15 minutes
  }

  await this.save();
};

// Method to handle successful login
userSchema.methods.handleSuccessfulLogin = async function (): Promise<void> {
  this.failed_login_attempts = 0;
  this.account_locked_until = undefined;
  this.last_login_at = new Date();
  await this.save();
};

// Method to check if account is locked
userSchema.methods.isAccountLocked = function (): boolean {
  return !!(
    this.account_locked_until && this.account_locked_until > new Date()
  );
};

// Method to get remaining lock time in minutes
userSchema.methods.getRemainingLockTime = function (): number {
  if (!this.account_locked_until) return 0;
  const remaining = Math.ceil(
    (this.account_locked_until.getTime() - Date.now()) / (60 * 1000)
  );
  return remaining > 0 ? remaining : 0;
};

// Method to generate JWT access token
userSchema.methods.generateAuthToken = function (): string {
  const payload = {
    userId: this._id.toString(),
    email: this.email,
    taxpayer_id: this.taxpayer_id,
  };

  return jwt.sign(payload, process.env.JWT_SECRET || "your-secret-key", {
    expiresIn: process.env.JWT_EXPIRES_IN || "15m",
  } as jwt.SignOptions);
};

// Method to generate JWT refresh token
userSchema.methods.generateRefreshToken = function (): string {
  const payload = {
    userId: this._id.toString(),
    type: "refresh",
  };

  return jwt.sign(
    payload,
    process.env.JWT_REFRESH_SECRET || "your-refresh-secret",
    {
      expiresIn: process.env.JWT_REFRESH_EXPIRES_IN || "7d",
    } as jwt.SignOptions
  );
};

// Override toJSON to exclude sensitive fields
userSchema.methods.toJSON = function () {
  const user = this.toObject();
  delete user.password_hash;
  delete user.refresh_tokens;
  delete user.email_verification_token;
  delete user.email_verification_expires;
  delete user.password_reset_token;
  delete user.password_reset_expires;
  delete user.__v;
  return user;
};

/**
 * User Model
 */
export const User = mongoose.model<IUser>("User", userSchema);
