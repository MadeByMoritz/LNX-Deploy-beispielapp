/* SPDX-License-Identifier: MIT */
/* HTMX ohne eval und ohne eingefügte Styles; keine Inline-Skripte (CSP). */
if (window.htmx) {
  window.htmx.config.allowEval = false;
  window.htmx.config.allowScriptTags = false;
  window.htmx.config.includeIndicatorStyles = false;
}
