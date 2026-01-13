import mongoose, { Schema } from "mongoose";
import type { IBusiness, IAddress } from "../types/business.types.js";

/**
 * Mongoose schema for Address (subdocument)
 */
const addressSchema = new Schema<IAddress>(
  {
    street_name: {
      type: String,
      required: [true, "Street name is required"],
      trim: true,
    },
    city_name: {
      type: String,
      required: [true, "City name is required"],
      trim: true,
    },
    postal_zone: {
      type: String,
      required: [true, "Postal zone is required"],
      trim: true,
    },
    country_code: {
      type: String,
      required: [true, "Country code is required"],
      trim: true,
      uppercase: true,
      minlength: 2,
      maxlength: 2,
    },
    local_government_code: {
      type: String,
      trim: true,
    },
    state_code: {
      type: String,
      trim: true,
    },
  },
  { _id: false } // Prevent creating _id for subdocument
);

/**
 * Mongoose schema for Business
 */
const businessSchema = new Schema<IBusiness>(
  {
    taxpayer_id: {
      type: String,
      required: [true, "Taxpayer ID is required"],
      trim: true,
      index: true,
    },
    taxpayer_name: {
      type: String,
      required: [true, "Taxpayer name is required"],
      trim: true,
    },
    taxpayer_email: {
      type: String,
      required: [true, "Taxpayer email is required"],
      lowercase: true,
      trim: true,
    },
    tax_identification_number: {
      type: String,
      required: [true, "Tax identification number is required"],
      unique: true,
      trim: true,
      index: true,
    },
    address: {
      type: addressSchema,
      required: [true, "Address is required"],
    },
    active: {
      type: Boolean,
      default: true,
      index: true,
    },
    is_test: {
      type: Boolean,
      default: false,
      index: true,
    },
    service_id: {
      type: String,
      trim: true,
    },
    firs_business_id: {
      type: String,
      trim: true,
      sparse: true, // Allow multiple null values, but unique if set
      index: true,
    },
    encrypted_crypto_keys: {
      type: String,
      select: false, // Never include in queries by default for security
      trim: true,
    },
  },
  {
    timestamps: {
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
    collection: "businesses",
  }
);

// Compound indexes for common queries
businessSchema.index({ taxpayer_id: 1, active: 1 });
businessSchema.index({ tax_identification_number: 1, active: 1 });
businessSchema.index({ is_test: 1, active: 1 });

// Virtual for user reference (if needed later)
businessSchema.virtual("user", {
  ref: "User",
  localField: "taxpayer_id",
  foreignField: "taxpayer_id",
  justOne: true,
});

/**
 * Business Model
 */
export const Business = mongoose.model<IBusiness>("Business", businessSchema);
