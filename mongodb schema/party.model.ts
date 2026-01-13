import mongoose, { Schema } from "mongoose";
import type { IParty, IPartyAddress } from "../types/party.types.js";

/**
 * Mongoose schema for Party Address (subdocument)
 */
const partyAddressSchema = new Schema<IPartyAddress>(
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
      maxlength: 3,
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
 * Mongoose schema for Party
 */
const partySchema = new Schema<IParty>(
  {
    business_id: {
      type: Schema.Types.ObjectId,
      ref: "Business",
      required: [true, "Business ID is required"],
      index: true,
    },
    tax_identification_number: {
      type: String,
      required: [true, "Tax identification number is required"],
      trim: true,
      index: true,
    },
    email: {
      type: String,
      required: [true, "Email is required"],
      lowercase: true,
      trim: true,
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
    address: {
      type: partyAddressSchema,
      required: [true, "Address is required"],
    },
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
    collection: "parties",
  }
);

// Compound indexes for common queries
partySchema.index({ business_id: 1, active: 1 });
partySchema.index({ business_id: 1, tax_identification_number: 1 });
partySchema.index({ business_id: 1, email: 1 });

// Ensure unique TIN per business (same party can't be added twice to same business)
partySchema.index(
  { business_id: 1, tax_identification_number: 1 },
  { unique: true }
);

// Virtual for business reference
partySchema.virtual("business", {
  ref: "Business",
  localField: "business_id",
  foreignField: "_id",
  justOne: true,
});

/**
 * Party Model
 */
export const Party = mongoose.model<IParty>("Party", partySchema);
