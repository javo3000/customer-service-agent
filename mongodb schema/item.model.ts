import mongoose, { Schema } from "mongoose";
import type { IItem } from "../types/item.types.js";

/**
 * Mongoose schema for Item
 */
const itemSchema = new Schema<IItem>(
  {
    business_id: {
      type: Schema.Types.ObjectId,
      ref: "Business",
      required: [true, "Business ID is required"],
      index: true,
    },
    tax_category_code: {
      type: String,
      required: [true, "Tax category code is required"],
      trim: true,
      index: true,
    },
    product_category: {
      type: String,
      required: [true, "Product category is required"],
      trim: true,
      index: true,
    },
    item_name: {
      type: String,
      required: [true, "Item name is required"],
      trim: true,
    },
    hsn_code: {
      type: String,
      required: [true, "HSN code is required"],
      trim: true,
      index: true,
    },
    description: {
      type: String,
      required: [true, "Description is required"],
      trim: true,
    },
    display_name: {
      type: String,
      trim: true,
    },
    item_code: {
      type: String,
      trim: true,
      index: true,
    },
    is_service: {
      type: Boolean,
      required: [true, "Is service flag is required"],
      index: true,
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
    collection: "items",
  }
);

// Compound indexes for common queries
itemSchema.index({ business_id: 1, active: 1 });
itemSchema.index({ business_id: 1, item_code: 1 });
itemSchema.index({ business_id: 1, is_service: 1 });
itemSchema.index({ business_id: 1, product_category: 1 });

// Virtual for business reference
itemSchema.virtual("business", {
  ref: "Business",
  localField: "business_id",
  foreignField: "_id",
  justOne: true,
});

/**
 * Item Model
 */
export const Item = mongoose.model<IItem>("Item", itemSchema);
