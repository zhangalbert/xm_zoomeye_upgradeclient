CREATE TABLE IF NOT EXISTS "upgradeclient" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "log_level" text DEFAULT '',
  "log_name" text DEFAULT '',
  "log_class" text DEFAULT '',
  "dao_name" text DEFAULT '',
  "file_type" text DEFAULT '',
  "file_name" text DEFAULT '',
  "file_url" text DEFAULT '',
  "last_author" text DEFAULT '' ,
  "last_date" text DEFAULT '',
  "last_revision" text DEFAULT '',
  "last_action" text DEFAULT '',
  "log_message" text DEFAULT '',
  "created_time" TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

