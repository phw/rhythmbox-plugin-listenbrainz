project('rhythmbox-plugin-listenbrainz',
  version: '1.2.4',
)

install_data('listenbrainz/schema/org.gnome.rhythmbox.plugins.listenbrainz.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

install_subdir('listenbrainz',
  install_dir: join_paths(get_option('libdir'), 'rhythmbox/plugins'),
  exclude_directories: ['schema'],
  exclude_files: ['settings.ui']
)

install_data('listenbrainz/settings.ui',
  install_dir: join_paths(get_option('datadir'), 'rhythmbox/plugins')
)
