```bash
sudo -u postgres createdb landscape-standalone-task-handler
sudo -u postgres psql landscape-standalone-task-handler -c \
  "GRANT CONNECT ON DATABASE \"landscape-standalone-task-handler\" TO landscape;"
sudo -u postgres psql landscape-standalone-task-handler -c \
  "GRANT CREATE ON SCHEMA public TO landscape;"
```
