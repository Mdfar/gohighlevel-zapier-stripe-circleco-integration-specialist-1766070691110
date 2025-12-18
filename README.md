GHL to Circle.so Automation Bridge

This project provides a centralized, code-based alternative to Zapier for managing complex, conditional onboarding for the "Stop Drinking Coach" funnel.

Features

Centralized Mapping: Manage product-to-space relationships in a single config.json file.

Conditional Logic: Automatically identifies main offers vs. bumps/upsells to grant granular access.

GHL Tagging: Applies specific tags to trigger GoHighLevel's internal email sequences for upsell/downsell logic.

Error Handling: Log-based tracking of API successes and failures.

Setup Instructions

Host the App: Deploy this to a service like Render, Heroku, or a VPS.

Configure Environment: Rename .env.example to .env and add your API keys.

Map Products: Update config.json with your GHL/Stripe Product IDs and corresponding Circle Space IDs.

Set Webhook: In GoHighLevel, create a Workflow triggered by "Order Submitted". Add a "Webhook" action pointing to https://your-app-url.com/webhook/purchase.

How it works

When a purchase occurs, the script:

Receives the product list.

Cross-references the list against config.json.

Calls the Circle.so API to add the member to the appropriate spaces.

Calls the GHL API to apply tags, which triggers your post-purchase email flows.