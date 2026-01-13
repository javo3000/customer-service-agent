import mongoose, { Schema } from "mongoose";
import type {
  IInvoice,
  IPostalAddress,
  IParty,
  IDocumentReference,
  IInvoiceDeliveryPeriod,
  IPaymentMeans,
  IAllowanceCharge,
  ITaxCategory,
  ITaxSubtotal,
  ITaxTotal,
  ILegalMonetaryTotal,
  IInvoiceItem,
  IInvoicePrice,
  IInvoiceLine,
} from "../types/invoice.types.js";

/**
 * Postal Address Schema (subdocument)
 */
const postalAddressSchema = new Schema<IPostalAddress>(
  {
    street_name: { type: String, required: true, trim: true },
    city_name: { type: String, required: true, trim: true },
    postal_zone: { type: String, required: true, trim: true },
    country: { type: String, required: true, trim: true },
    local_government_code: { type: String, trim: true },
    state_code: { type: String, trim: true },
  },
  { _id: false }
);

/**
 * Party Schema (subdocument)
 */
const partySchema = new Schema<IParty>(
  {
    party_name: { type: String, required: true, trim: true },
    tin: { type: String, required: true, trim: true },
    email: { type: String, required: true, lowercase: true, trim: true },
    telephone: { type: String, required: true, trim: true },
    business_description: { type: String, required: true, trim: true },
    postal_address: { type: postalAddressSchema, required: true },
  },
  { _id: false }
);

/**
 * Document Reference Schema (subdocument)
 */
const documentReferenceSchema = new Schema<IDocumentReference>(
  {
    issue_date: { type: String, required: true },
    irn: { type: String },
  },
  { _id: false }
);

/**
 * Invoice Delivery Period Schema (subdocument)
 */
const invoiceDeliveryPeriodSchema = new Schema<IInvoiceDeliveryPeriod>(
  {
    start_date: { type: String, required: true },
    end_date: { type: String, required: true },
  },
  { _id: false }
);

/**
 * Payment Means Schema (subdocument)
 */
const paymentMeansSchema = new Schema<IPaymentMeans>(
  {
    payment_means_code: { type: String, required: true },
    payment_due_date: { type: String, required: true },
  },
  { _id: false }
);

/**
 * Allowance/Charge Schema (subdocument)
 */
const allowanceChargeSchema = new Schema<IAllowanceCharge>(
  {
    charge_indicator: { type: Boolean, required: true },
    amount: { type: Number, required: true },
  },
  { _id: false }
);

/**
 * Tax Category Schema (subdocument)
 */
const taxCategorySchema = new Schema<ITaxCategory>(
  {
    id: { type: String, required: true },
    percent: { type: Number, required: true },
  },
  { _id: false }
);

/**
 * Tax Subtotal Schema (subdocument)
 */
const taxSubtotalSchema = new Schema<ITaxSubtotal>(
  {
    taxable_amount: { type: Number, required: true },
    tax_amount: { type: Number, required: true },
    tax_category: { type: taxCategorySchema, required: true },
  },
  { _id: false }
);

/**
 * Tax Total Schema (subdocument)
 */
const taxTotalSchema = new Schema<ITaxTotal>(
  {
    tax_amount: { type: Number, required: true },
    tax_subtotal: { type: [taxSubtotalSchema], required: true },
  },
  { _id: false }
);

/**
 * Legal Monetary Total Schema (subdocument)
 */
const legalMonetaryTotalSchema = new Schema<ILegalMonetaryTotal>(
  {
    line_extension_amount: { type: Number, required: true },
    tax_exclusive_amount: { type: Number, required: true },
    tax_inclusive_amount: { type: Number, required: true },
    allowance_total_amount: { type: Number },
    charge_total_amount: { type: Number },
    payable_amount: { type: Number, required: true },
  },
  { _id: false }
);

/**
 * Invoice Item Schema (subdocument)
 */
const invoiceItemSchema = new Schema<IInvoiceItem>(
  {
    name: { type: String, required: true, trim: true },
    description: { type: String, required: true, trim: true },
    sellers_item_identification: { type: String, required: true, trim: true },
  },
  { _id: false }
);

/**
 * Invoice Price Schema (subdocument)
 */
const invoicePriceSchema = new Schema<IInvoicePrice>(
  {
    price_amount: { type: Number, required: true },
    base_quantity: { type: Number, required: true },
    price_unit: { type: String, required: true, trim: true },
  },
  { _id: false }
);

/**
 * Invoice Line Schema (subdocument)
 */
const invoiceLineSchema = new Schema<IInvoiceLine>(
  {
    hsn_code: { type: String, required: true, trim: true },
    product_category: { type: String, required: true, trim: true },
    discount_rate: { type: Number },
    discount_amount: { type: Number },
    fee_rate: { type: Number },
    fee_amount: { type: Number },
    invoiced_quantity: { type: Number, required: true },
    line_extension_amount: { type: Number, required: true },
    item: { type: invoiceItemSchema, required: true },
    price: { type: invoicePriceSchema, required: true },
  },
  { _id: false }
);

/**
 * Main Invoice Schema
 */
const invoiceSchema = new Schema<IInvoice>(
  {
    business_id: {
      type: Schema.Types.ObjectId,
      ref: "Business",
      required: [true, "Business ID is required"],
      index: true,
    },
    party_id: {
      type: Schema.Types.ObjectId,
      ref: "Party",
      required: [true, "Party ID is required"],
      index: true,
    },

    // Invoice identifiers
    irn: {
      type: String,
      required: [true, "IRN is required"],
      trim: true,
      unique: true, // IRN must be unique across all invoices
      index: true,
      // Format: {invoice_number}-{service_id}-{YYYYMMDD}
      // Generated by concatenating invoice_number + service_id + datestamp
    },
    invoice_number: {
      type: String,
      trim: true,
      index: true,
      // Optional - from user's accounting system OR auto-generated as INVYY####
      // Format: INV + YY (year) + #### (sequential per year, 0001-9999)
      // Examples: INV240001, INV240002, INV250001 (resets yearly)
    },
    issue_date: {
      type: String,
      required: [true, "Issue date is required"],
      index: true,
    },
    due_date: { type: String },
    issue_time: { type: String },
    invoice_type_code: {
      type: String,
      required: [true, "Invoice type code is required"],
      trim: true,
    },

    // Payment information
    payment_status: {
      type: String,
      enum: ["pending", "partial", "paid", "overdue", "cancelled"],
      default: "pending",
      index: true,
    },
    payment_date: { type: String },

    // Additional metadata
    note: { type: String, trim: true },
    tax_point_date: { type: String },
    document_currency_code: {
      type: String,
      required: [true, "Document currency code is required"],
      trim: true,
      uppercase: true,
    },
    tax_currency_code: { type: String, trim: true, uppercase: true },
    accounting_cost: { type: String, trim: true },
    buyer_reference: { type: String, trim: true },

    // Delivery and reference information
    invoice_delivery_period: { type: invoiceDeliveryPeriodSchema },
    order_reference: { type: String, trim: true },
    billing_reference: { type: [documentReferenceSchema] },
    dispatch_document_reference: { type: documentReferenceSchema },
    receipt_document_reference: { type: documentReferenceSchema },
    originator_document_reference: { type: documentReferenceSchema },
    contract_document_reference: { type: documentReferenceSchema },
    additional_document_reference: { type: [documentReferenceSchema] },
    actual_delivery_date: { type: String },

    // Parties
    accounting_supplier_party: {
      type: partySchema,
      required: [true, "Supplier party is required"],
    },
    accounting_customer_party: {
      type: partySchema,
      required: [true, "Customer party is required"],
    },

    // Payment terms
    payment_means: { type: [paymentMeansSchema] },
    payment_terms_note: { type: String, trim: true },

    // Charges and allowances
    allowance_charge: {
      type: [allowanceChargeSchema],
      required: true,
      default: [],
    },

    // Tax information
    tax_total: { type: [taxTotalSchema] },

    // Monetary totals
    legal_monetary_total: {
      type: legalMonetaryTotalSchema,
      required: [true, "Legal monetary total is required"],
    },

    // Invoice lines
    invoice_line: {
      type: [invoiceLineSchema],
      required: [true, "At least one invoice line is required"],
      validate: {
        validator: function (lines: IInvoiceLine[]) {
          return lines && lines.length > 0;
        },
        message: "Invoice must have at least one line item",
      },
    },

    // NRS submission tracking
    firs_status: {
      type: String,
      enum: ["draft", "pending", "complete", "transmitted", "failed"],
      default: "draft",
      index: true,
      // draft: Invoice created, IRN generated locally
      // pending: Validation request sent to NRS, QR code generated
      // complete: Invoice signed and submitted to NRS, downloadable
      // transmitted: Invoice sent to receiving party (if endpoint registered)
      // failed: NRS submission/validation failed
    },
    firs_validation_date: { type: Date }, // When validation request was sent
    firs_completion_date: { type: Date }, // When invoice was signed and completed
    firs_submission_date: { type: Date }, // When transmitted to receiving party
    firs_response: { type: Schema.Types.Mixed }, // Store NRS API responses
    firs_qr_code: { type: String }, // QR code URL/data from NRS
    callback_url: { type: String, trim: true }, // Webhook URL for status notifications

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
    collection: "invoices",
  }
);

// Compound indexes for common queries
invoiceSchema.index({ business_id: 1, active: 1 });
invoiceSchema.index({ business_id: 1, payment_status: 1 });
invoiceSchema.index({ business_id: 1, issue_date: -1 });
invoiceSchema.index({ party_id: 1, active: 1 });
invoiceSchema.index({ invoice_number: 1 }); // Simple index, not unique
invoiceSchema.index({ irn: 1 }, { unique: true }); // IRN is unique across all invoices
invoiceSchema.index({ firs_status: 1, active: 1 });

// Virtual for business reference
invoiceSchema.virtual("business", {
  ref: "Business",
  localField: "business_id",
  foreignField: "_id",
  justOne: true,
});

// Virtual for party reference
invoiceSchema.virtual("party", {
  ref: "Party",
  localField: "party_id",
  foreignField: "_id",
  justOne: true,
});

/**
 * Invoice Model
 */
export const Invoice = mongoose.model<IInvoice>("Invoice", invoiceSchema);
