**Apache**

If Apache isn't already listening on port 8000, add `Listen 8000` to `/etc/apache2/ports.conf` (or another included config file) before enabling the site.

Install the file below as `/etc/apache2/sites-available/filesystem-repo.conf` and change the following values:

- `@hostname@`: The fully qualified domain name for your server.
- `@publication_target_file_path@`: The full path of the published repository directory, which is the published root joined with the path you chose when creating the filesystem publication target (e.g. `/srv/published-repos/myrepo/ubuntu`).

```apache
<VirtualHost *:8000>
    ServerName @hostname@

    DocumentRoot @publication_target_file_path@

    <Directory @publication_target_file_path@>
        Options +Indexes

        # Optional: Makes the directory listings look a bit cleaner
        IndexOptions FancyIndexing NameWidth=* FoldersFirst
        
        Require all granted
    </Directory>

    # Optional: Logging configuration for easier troubleshooting
    ErrorLog /var/log/apache2/repo_error.log
    CustomLog /var/log/apache2/repo_access.log combined
</VirtualHost>
```

Then enable it:

```bash
sudo a2ensite filesystem-repo.conf
```

And restart Apache:

```bash
sudo systemctl restart apache2
```

**Nginx**

Create `/etc/nginx/sites-available/filesystem-repo.conf` with the following contents, then replace:

- `<YOUR_FQDN>`: The fully qualified domain name for your server.
- `<PUBLICATION_TARGET_FILE_PATH>`: The full path of the published repository directory, which is the published root joined with the path you chose when creating the filesystem publication target (e.g. `/srv/published-repos/myrepo/ubuntu`).

```nginx
server {
    listen 8000;
    listen [::]:8000;

    server_name <YOUR_FQDN>;

    root <PUBLICATION_TARGET_FILE_PATH>;

    location / {
        autoindex on;
        
        # Optional: Makes the directory listings look a bit cleaner
        autoindex_exact_size off;
        autoindex_localtime on;

        try_files $uri $uri/ =404;
    }

    # Optional: Logging configuration for easier troubleshooting
    access_log /var/log/nginx/repo_access.log;
    error_log /var/log/nginx/repo_error.log;
}
```

Then enable it:

```bash
sudo ln -s /etc/nginx/sites-available/filesystem-repo.conf /etc/nginx/sites-enabled/
```

And restart Nginx:

```bash
sudo systemctl restart nginx
```
