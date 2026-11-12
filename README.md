# Muscle Health landing page

Static technology-licensing page. `index.html` is the approved copy source; `styles.css`, `typography.css`, `buttons.css` and `theme.css` provide the layout and coral theme. `app.js` handles navigation, video playback. `assets/` contains only used media and fonts.

## Preview and handoff

- `npm run dev`: standalone preview at http://127.0.0.1:4178/.
- `npm run build:webflow`: regenerate the isolated Webflow bundle after source changes.
- `npm run check`: check source and generated JavaScript syntax.
- Preview the bundle at http://127.0.0.1:4178/webflow/preview.html.

Sasha: follow [Webflow setup](documentation/webflow-setup.txt) and [Microsoft Bookings / Outlook](documentation/microsoft-bookings.md). The scheduler uses the company introduction-meeting link.

Before publication, verify the final hosted assets, booking availability, mobile layout and keyboard navigation. Remove the standalone `noindex,nofollow` only when indexing is approved; set Webflow metadata separately. No deployment or appointments are created by these files.

[Asset sources](documentation/asset-sources.md). Poppins license: `assets/fonts/OFL.txt`.
