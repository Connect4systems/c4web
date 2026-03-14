# c4web

Full Arabic RTL redesign for `connect4systems.com` as an installable Frappe app.

This repository now contains the **Phase 2 full version**:
- Professional interactive frontend
- Rewritten Arabic content
- Sector pages for trade, retail, CRM, factory, and HR
- AI-first brand positioning (`80%` AI-enabled team workflow)
- Legacy URL route mapping for key old pages

## App Structure

- `c4web/public/css/style.css`: Shared design system (RTL, responsive, interactive)
- `c4web/public/js/app.js`: Shared behavior (menu, reveal, counters, tabs, filters, accordion)
- `c4web/www/index.html`: New homepage
- `c4web/www/solution-template.html`: Solutions hub
- `c4web/www/trade.html`: Trade sector page
- `c4web/www/retail-system.html`: Retail sector page
- `c4web/www/crm.html`: CRM sector page
- `c4web/www/factory.html`: Factory sector page
- `c4web/www/hr.html`: HR sector page
- `c4web/www/catalog.html`: Packages + full verified media gallery
- `c4web/www/blog-list.html`: Blog listing with filters
- `c4web/www/blog-post.html`: Featured article page
- `c4web/www/about.html`: Company profile page
- `c4web/www/contact.html`: Conversion-focused contact page
- `c4web/hooks.py`: App metadata + route rules from legacy URLs to new pages

## Planning And Inventory Docs

- `docs/redesign-backlog-ar-rtl.md`: rollout backlog
- `docs/sitemap-links.txt`: sitemap export
- `docs/redirect-seed.csv`: redirect seed map
- `docs/image-inventory-verified.txt`: verified image URLs used in the redesign

## GitHub Authentication

> **GitHub no longer accepts your account password for git operations.**
> Since August 2021, you must use either an **SSH key** or a **Personal Access Token (PAT)**.
> If you are prompted for a username/password and then see
> `remote: Support for password authentication was removed`, follow one of the two options below.

---

### Option A — SSH key (recommended for servers)

**Step 1 – generate a key on your server (if you don't already have one)**

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
# Press Enter to accept the default path (~/.ssh/id_ed25519)
# Set a passphrase or leave blank
```

**Step 2 – copy the public key**

```bash
cat ~/.ssh/id_ed25519.pub
```

**Step 3 – add the public key to GitHub**

1. Go to **GitHub → your profile → Settings → SSH and GPG keys → New SSH key**
2. Paste the output of the command above and save.

**Step 4 – switch the remote URL to SSH**

```bash
cd ~/frappe-bench/apps/c4web

# Check current remote URL
git remote -v

# Replace the HTTPS URL with the SSH URL
git remote set-url origin git@github.com:Connect4systems/c4web.git

# Verify
git remote -v
```

**Step 5 – pull as normal**

```bash
git pull origin main
```

---

### Option B — Personal Access Token (PAT)

If you prefer HTTPS, replace your GitHub password with a PAT.

**Step 1 – create a token on GitHub**

1. Go to **GitHub → your profile → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token**
2. Give it a name (e.g. "server-c4web"), set an expiration, and tick the **`repo`** scope.
3. Click **Generate token** and copy it immediately — GitHub will not show it again.

**Step 2 – use the token when git asks for a password**

When you run `git pull` (or `bench get-app`), enter:

- **Username**: your GitHub username (e.g. `Connect4systems`)
- **Password**: paste the PAT you just copied (NOT your GitHub account password)

**Step 3 (optional) – save the token so you are not asked again**

```bash
git config --global credential.helper store
# Run git pull once more; enter credentials once; they are saved to ~/.git-credentials
git pull origin main
```

---

## Bench Install (first time)

> **Authentication required.** Before running `bench get-app`, make sure you have set up
> either an SSH key or a PAT as described in the [GitHub Authentication](#github-authentication) section above.

**Using SSH (recommended):**

```bash
cd ~/frappe-bench
rm -rf apps/c4web   # remove any old copy first

bench get-app git@github.com:Connect4systems/c4web.git
bench --site <your-site-name> install-app c4web
bench --site <your-site-name> migrate
bench build
bench clear-cache
bench --site <your-site-name> clear-website-cache
bench restart
```

**Using HTTPS + PAT:**

```bash
cd ~/frappe-bench
rm -rf apps/c4web

bench get-app https://github.com/Connect4systems/c4web
# When prompted: Username = your GitHub username, Password = your PAT
bench --site <your-site-name> install-app c4web
bench --site <your-site-name> migrate
bench build
bench clear-cache
bench --site <your-site-name> clear-website-cache
bench restart
```

## Updating the Site (pulling latest changes)

### Normal update (app was cloned with `bench get-app`)

```bash
cd ~/frappe-bench/apps/c4web
git pull origin main

cd ~/frappe-bench
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

### Fix: `fatal: 'origin' does not appear to be a git repository`

This error means the remote URL was never configured (or the app was copied manually instead of cloned). Run the following to add the remote and then pull:

```bash
cd ~/frappe-bench/apps/c4web

# Check current remotes (may be empty)
git remote -v

# Add the GitHub remote (SSH – no password needed)
git remote add origin git@github.com:Connect4systems/c4web.git

# Fetch and pull the latest code
git fetch origin
git pull origin main

# Back to bench root – clear cache and restart
cd ~/frappe-bench
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

### Fix: directory is not a git repository at all

If `apps/c4web` was extracted from a zip or copied manually it has no `.git` folder. The safest fix is a clean re-install:

```bash
cd ~/frappe-bench

# Remove the manually-copied directory
rm -rf apps/c4web

# Re-clone via bench using SSH (no password prompt)
bench get-app git@github.com:Connect4systems/c4web.git

# No need to re-run install-app if the site already has c4web installed
bench --site <your-site-name> clear-cache
bench --site <your-site-name> clear-website-cache
bench build --app c4web
bench restart
```

## Development Notes

- All pages are authored with `lang="ar" dir="rtl"`.
- Legacy links like `/home`, `/all-products`, `/retais-erp`, `/hr2`, and key `/blog/*` category routes are mapped in `c4web/hooks.py`.
- The catalog page includes the full verified image set to satisfy the full-asset usage requirement.
