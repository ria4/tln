#!/usr/bin/python

import sqlite3
import sys

def open_db(nam):
    conn = sqlite3.connect(nam)
    # Let rows returned be of dict/tuple type
    conn.row_factory = sqlite3.Row
    print("Opened database %s as %r" % (nam, conn))
    return conn

def copy_table(table, src, dest):
    print("Copying %s %s => %s" % (table, src, dest))
    sc = src.execute('SELECT * FROM %s' % table)
    ins = None
    dc = dest.cursor()
    for row in sc.fetchall():
        if not ins:
            cols = tuple([k for k in row.keys() if k != 'id'])
            len_cols = len(cols)
            if len(cols) == 1:
                cols = "('%s')" % cols[0]
                len_cols = 1
            ins = 'INSERT OR REPLACE INTO %s %s VALUES (%s)' % (table, cols,
                                                     ','.join(['?'] * len_cols))
            print('INSERT stmt = ' + ins)
            if len_cols == 1:
                cols = (cols[2:-2],)
        c = [row[c] for c in cols]
        dc.execute(ins, c)

    dest.commit()

src_conn  = open_db(sys.argv[1])
dest_conn = open_db(sys.argv[2])

copy_table('auth_group', src_conn, dest_conn)
copy_table('auth_group_permissions', src_conn, dest_conn)
copy_table('auth_user_groups', src_conn, dest_conn)
copy_table('auth_user_user_permissions', src_conn, dest_conn)
copy_table('django_admin_log', src_conn, dest_conn)
copy_table('django_content_type', src_conn, dest_conn)
copy_table('auth_permission', src_conn, dest_conn)
copy_table('auth_user', src_conn, dest_conn)
copy_table('django_session', src_conn, dest_conn)
copy_table('django_comment_flags', src_conn, dest_conn)
copy_table('django_comments', src_conn, dest_conn)
copy_table('django_site', src_conn, dest_conn)
copy_table('tagging_taggeditem', src_conn, dest_conn)
copy_table('tagging_tag', src_conn, dest_conn)
copy_table('zinnia_entry_categories', src_conn, dest_conn)
copy_table('zinnia_entry_related', src_conn, dest_conn)
copy_table('zinnia_entry_sites', src_conn, dest_conn)
copy_table('zinnia_entry_authors', src_conn, dest_conn)
copy_table('photologue_watermark', src_conn, dest_conn)
copy_table('photologue_photosize', src_conn, dest_conn)
copy_table('photologue_gallery_photos', src_conn, dest_conn)
copy_table('photologue_gallery_sites', src_conn, dest_conn)
copy_table('photologue_photo_sites', src_conn, dest_conn)
copy_table('photologue_gallery', src_conn, dest_conn)
copy_table('photologue_photo', src_conn, dest_conn)
copy_table('photos_gallerycustom', src_conn, dest_conn)
copy_table('photos_photocustom', src_conn, dest_conn)
copy_table('photologue_photoeffect', src_conn, dest_conn)
copy_table('photos_gallerycustom_allowed_users', src_conn, dest_conn)
copy_table('zinnia_entry', src_conn, dest_conn)
copy_table('zinnia_category', src_conn, dest_conn)
