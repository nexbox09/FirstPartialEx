# Enabling Brotli Compression for Unity Web Builds on Apache (CentOS)

This README provides a step-by-step guide to enable Brotli compression for Unity Web builds served by an Apache 2.4.6 web server on CentOS.  Brotli compression significantly improves loading times for users by reducing the size of transferred files.

## Objective

To configure an Apache 2.4.6 server on CentOS to serve Brotli-compressed Unity Web builds.

## Prerequisites

*   A CentOS system with Apache 2.4.6 installed.
*   Root or `sudo` access to the server.
*   A Unity Web build (with Brotli compression enabled during the build process in Unity's build settings).
*   Basic familiarity with the command line and text editors (e.g., `nano` or `vim`).

## Procedure

### Part 1: Install and Configure `mod_brotli`

1.  **Check for Existing `mod_brotli`:**

    Open a terminal and run:

    ```bash
    apachectl -M | grep brotli
    ```
    or
    ```bash
    httpd -M | grep brotli
    ```

    *   If the output includes `brotli_module (shared)`, the module is already installed and loaded.  Proceed to Part 2.
    *   If the output is empty, the module is *not* installed. Continue to step 2.

2.  **Install `mod_brotli` (if needed):**

    On CentOS, use the EPEL repository:

    ```bash
    sudo yum install epel-release -y  # Enable EPEL (if not already enabled)
    sudo yum install mod_brotli -y
    ```

3.  **Verify Installation:**

    Run the check command again:

    ```bash
    apachectl -M | grep brotli
    ```
    or
    ```bash
    httpd -M | grep brotli
    ```

    Confirm that `brotli_module (shared)` is now listed in the output.

4.  **Restart Apache:**

    Restart Apache for the new module to be loaded:

    ```bash
    sudo systemctl restart httpd
    ```

### Part 2: Configure Apache (httpd.conf Method - Recommended)

1.  **Locate `httpd.conf`:**

    The `httpd.conf` file is usually in one of these locations:

    *   `/etc/httpd/conf/httpd.conf` (most common on CentOS)
    *   `/etc/apache2/httpd.conf` (less common on CentOS)
    *   `/usr/local/apache2/conf/httpd.conf` (if Apache was installed from source)

    If you're unsure, you can try to find it:

    ```bash
    sudo find / -name httpd.conf 2>/dev/null
    ```

2.  **Edit `httpd.conf`:**

    Open `httpd.conf` with a text editor, using `sudo` for write access:

    ```bash
    sudo nano /etc/httpd/conf/httpd.conf  # Replace with the correct path
    ```

3.  **Find or Create the `<Directory>` Block:**

    You need to find the `<Directory>` block that corresponds to the root directory of your website, where your Unity Web build files are located.  The example in the original documentation is:

    ```apache
    <Directory /var/www/html/root/path/to/your/unity/content/>
        # ... configuration here ...
    </Directory>
    ```

    *   **Replace `/var/www/html/root/path/to/your/unity/content/` with the *actual* path to your Unity Web build files.**  For example, if your files are in `/var/www/html/mygame`, use `/var/www/html/mygame`.
    *   **If a `<Directory>` block for your website *doesn't* exist, create one at the *end* of the `httpd.conf` file:**

        ```apache
        <Directory /var/www/html/mygame>  # Replace with YOUR Unity build's path
            # Configuration directives will go here
        </Directory>
        ```

4.  **Add the Brotli Configuration (Inside the `<Directory>` Block):**

    Paste the following configuration *inside* the `<Directory>` block (either the existing one or the one you created).  This configuration includes Brotli, Gzip (for fallback), and optional sections for multithreading and CORS:

    ```apache
    <IfModule mod_mime.c>
        # --- Brotli Configuration ---
        RemoveType .br
        AddEncoding br .br
        AddType application/octet-stream .data.br
        AddType application/wasm .wasm.br
        AddType application/javascript .js.br
        AddType application/octet-stream .symbols.json.br

        # --- Gzip Configuration (Optional, but recommended for wider compatibility) ---
        RemoveType .gz
        AddEncoding gzip .gz
        AddType application/gzip .data.gz  # Workaround for a Safari bug
        AddType application/wasm .wasm.gz
        AddType application/javascript .js.gz
        AddType application/octet-stream .symbols.json.gz

        # --- For Unity Web builds with decompression fallback ---
        AddEncoding br .unityweb  # For Brotli
        AddEncoding gzip .unityweb # For Gzip (optional, but good to have)

    </IfModule>

    # --- Multithreading (Optional - Only include if your Unity project uses it) ---
    <FilesMatch "\.(htm|html|js|js.gz|js.br)$">
        Header add Cross-Origin-Opener-Policy "same-origin"
        Header add Cross-Origin-Embedder-Policy "require-corp"
        Header add Cross-Origin-Resource-Policy "cross-origin"
    </FilesMatch>

    # --- CORS (Optional - Only include if you need Cross-Origin Resource Sharing) ---
    Header add Access-Control-Allow-Origin "*"
    ```

    **Important Notes:**

    *   The `AddType application/wasm .wasm.br` line is *critical* for the browser to correctly interpret `.wasm.br` files.
    *   The Gzip configuration is optional but recommended for browsers that don't support Brotli.
    *   The Multithreading and CORS sections are *only* needed if your Unity project specifically requires them.  If you're unsure, you can add them later if you encounter issues.  The `Access-Control-Allow-Origin "*"` setting allows requests from *any* origin; for production, you should restrict this to specific origins for security.

5.  **Save and Close:** Save the changes to the `httpd.conf` file and close the text editor.

6.  **Check Configuration Syntax:**

    *Always* check your Apache configuration for syntax errors *before* restarting:

    ```bash
    sudo apachectl configtest
    ```
    or
    ```bash
    sudo httpd -t
    ```

    *   If you see "Syntax OK", you can proceed.
    *   If you see *any* errors, carefully review the `httpd.conf` file, paying close attention to the line numbers mentioned in the error message.  Fix the errors and run `configtest` again until you get "Syntax OK".

7.  **Restart Apache:**

    Restart Apache to apply the changes:

    ```bash
    sudo systemctl restart httpd
    ```

### Part 3: Troubleshooting and the `mime.types` Fix

1.  **Test the Configuration:**

    *   **Clear Browser Cache:**  It's *essential* to clear your browser's cache or use an incognito/private browsing window to ensure you're not loading old, cached files.
    *   **Access Your Unity Web Build:** Open your web browser and navigate to the URL where your Unity Web build is hosted.
    *   **Use Developer Tools:**
        *   Open your browser's developer tools (usually by pressing F12).
        *   Go to the "Network" tab.
        *   Reload the page (Ctrl+Shift+R or Cmd+Shift+R for a hard reload).
        *   Inspect the HTTP headers for your `.data.br`, `.wasm.br`, and `.js.br` files:
            *   **`Content-Encoding`:** You should see `br` for these files, indicating Brotli compression.
            *   **`Content-Type`:**
                *   `.data.br`: `application/octet-stream`
                *   `.wasm.br`:  **`application/wasm`** (This is what we're troubleshooting)
                *   `.js.br`: `application/javascript`
                *   `.symbols.json.br`: `application/octet-stream`

2.  **If `Content-Type` for `.wasm.br` is Incorrect (Troubleshooting):**

    If you see the error "HTTP Response Header "Content-Type" configured incorrectly...", or the `Content-Type` for `.wasm.br` is *not* `application/wasm`, follow these steps:

    *   **Step 3.1 (Double-Check `AddType`):**

        Go back to your `httpd.conf` file and *meticulously* examine the `AddType` line for `.wasm.br`.  Ensure it looks *exactly* like this:

        ```apache
        AddType application/wasm .wasm.br
        ```

        *   **Case Sensitivity:**  `application/wasm` is case-sensitive.
        *   **Spacing:**  Ensure there's a single space between `application/wasm` and `.wasm.br`.
        *   **Typos:** Even a tiny typo will prevent it from working.
        * **Correct Block:** Verify that this line is within the `<IfModule mod_mime.c>` block, and that the entire block is inside the correct `<Directory>` block for your website.

    *   **Step 3.2 (Restart Apache and Clear Browser Cache):**

        After making *any* changes to `httpd.conf`, you *must* restart Apache:

        ```bash
        sudo systemctl restart httpd
        ```

        And, just as importantly, clear your browser's cache or use an incognito window.  The browser might be remembering the old, incorrect `Content-Type`.

     * **Step 3.3 Verify mod_mime is enabled:**
        ```bash
        apachectl -M | grep mime
        ```
        or
        ```bash
        httpd -M | grep mime
        ```
        Verify that the output shows: `mime_module (shared)`

    *   **Step 3.4 (System `mime.types` - The Key Fix):**

        If the `Content-Type` is *still* incorrect, the issue might be with your system's MIME type database.  Apache often uses a file (usually `/etc/mime.types`) to map file extensions to MIME types.

        *   **Locate `mime.types`:**

            ```bash
            sudo find / -name mime.types 2>/dev/null
            ```

            This will likely find one or more `mime.types` files.  The most important one is usually `/etc/mime.types`.

        *   **Edit `mime.types` (with Caution):**

            ```bash
            sudo nano /etc/mime.types  # Or the specific path found by the find command
            ```

        *   **Add the `application/wasm` Entry (if Missing):**

            Search for `application/wasm` within the file.  If it's *not* present, add this line:

            ```
            application/wasm                                wasm
            ```

            *   **Formatting:**  Make sure the line is formatted consistently with the other entries in the file (usually tab-separated, with the MIME type on the left and the extension(s) on the right).

        *   **Save and Close:**  Save the changes to the `mime.types` file and close the editor.

        *   **Restart Apache:**

            ```bash
            sudo systemctl restart httpd
            ```

    *   **Step 3.5 (Check for Conflicting Configurations):**

        If you have other Apache configuration files (e.g., virtual host files in `/etc/httpd/conf.d/`), check for any conflicting directives that might be overriding your `AddType` settings.  Look for other `AddType`, `RemoveType`, or `ForceType` directives that could affect `.wasm.br` files.

    *   **Step 3.6 (.htaccess Interference):**

        If you tried the `.htaccess` method *before* using `httpd.conf`, make sure there isn't an `.htaccess` file in your Unity build directory that is still present and interfering with your settings.  Either remove the `.htaccess` file entirely or ensure its contents are *exactly* what you intend and consistent with your `httpd.conf` configuration. If you are using httpd.conf, the `.htaccess` is unnecessary.

3.  **Retest:** After completing *any* of the troubleshooting steps, repeat the testing procedure in Step 1 of Part 3 (clear cache, access the build, check headers in developer tools).

## Key Considerations and Best Practices

*   **Caching:** Browser caching is a frequent cause of confusion during web server configuration. Always clear your browser's cache completely or use an incognito/private browsing window when testing changes.  A "hard reload" (Ctrl+Shift+R or Cmd+Shift+R) can often help.
*   **Syntax Errors:**  *Always* use `apachectl configtest` (or `httpd -t`) to check for syntax errors in your Apache configuration files *before* restarting Apache.  This prevents potential server downtime.
*   **`mod_mime`:** The `AddType` and `AddEncoding` directives *depend* on the `mod_mime` Apache module being enabled.  If you see errors related to these directives, ensure `mod_mime` is loaded.
*   **Unity Build Settings:** Confirm that your Unity project is configured to build with Brotli compression enabled in the build settings.
*   **File Paths:** Double-check all file paths in your configurations to make sure they are accurate.
*   **`httpd.conf` vs. `.htaccess`:**  Use `httpd.conf` (or virtual host configuration files) whenever possible.  The `.htaccess` method is primarily for situations where you don't have access to the main server configuration (e.g., shared hosting). `.htaccess` files can also impact performance.
* **SELinux (CentOS 8/9 and later):** If you encounter unexpected issues, SELinux (Security-Enhanced Linux) *might* be interfering. You can temporarily disable it for testing (`sudo setenforce 0`), but *do not* leave it disabled permanently. If disabling SELinux resolves the problem, you'll need to configure SELinux properly to allow Apache to access your files. This is a more advanced topic, and you should consult SELinux documentation or search for guides on configuring SELinux with web servers. Re-enable SELinux after testing (`sudo setenforce 1`).

This comprehensive guide should enable you to successfully configure Brotli compression for your Unity Web builds on Apache, resulting in faster loading times and a better user experience. Remember to test thoroughly after each configuration change.
