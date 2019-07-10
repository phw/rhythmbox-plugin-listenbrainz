project('rhythmbox-plugin-listenbrainz')

install_data('listenbrainz/schema/org.gnome.rhythmbox.plugins.listenbrainz.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

install_subdir('listenbrainz',
  install_dir: join_paths(get_option('datadir'), 'rhythmbox/plugins'),
  exclude_directories: [
    'schema'
  ]
)
