# Microsoft Bookings / Outlook

All `data-booking` links in `index.html` open the existing MeNow team scheduler in a new tab, using the company introduction-meeting scheduler. No HubSpot, popup, API keys or additional website integration is needed.

Scheduler: https://bookings.cloud.microsoft/book/MeNowintroductionmeeting@menow.ai/s/P_V2sdc3F0GJzpgIi8b1aA2?ismsaljsauthenabled

Sasha: verify this is the intended company booking page. If it changes, replace every `data-booking` href in `index.html`, run `npm run build:webflow`, and publish the updated bundle.

The company manages staff calendars, Outlook availability, appointment duration and confirmation emails in Microsoft Bookings. These settings are not controlled by the landing page. Verify a booking link and available appointments on staging before release; no test appointments have been made.
