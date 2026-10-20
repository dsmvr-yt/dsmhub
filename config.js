// Public values only. The Supabase anon key is safe in the browser because Row Level Security protects the data.
window.DSMHUB = {
  // jsDelivr: logo, favicon and icons load from cdn.jsdelivr.net/gh/<user>/<repo>@<ref>/assets/
  // Leave GITHUB_USER or GITHUB_REPO empty to load them from the site itself.
  GITHUB_USER: "",
  GITHUB_REPO: "",
  GITHUB_REF: "main",   // prefer a release tag or commit hash: branches are cached by jsDelivr for hours

  SUPABASE_URL: "",       // e.g. https://xxxx.supabase.co
  SUPABASE_ANON_KEY: ""
};
