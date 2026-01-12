project('{{ NEW_NAME }}',
  version: '{{ VERSION }}',
  meson_version: '>= 0.59.0',
  default_options: [
    'warning_level=2',
  ],
)

# Dependencies
gnome = import('gnome')
python = import('python')
i18n = import('i18n')


py_installation = python.find_installation('python3')

# Directories
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()

# Application ID
app_id = '{{ ID_NAME  }}'

# Python module installation
python_dir = py_installation.get_install_dir()

# Install Python package
install_subdir(
  'src/{{ NEW_NAME }}',
  install_dir: python_dir,
)

# Compile GResource
gnome.compile_resources(
  '{{ NEW_NAME }}',
  'src/{{ NEW_NAME }}/resources/{{ NEW_NAME }}.gresource.xml',
  source_dir: 'src/{{ NEW_NAME }}/resources',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# Install desktop file
desktop_file = i18n.merge_file(
        input: 'data/@0@.desktop.in'.format(app_id),
       output: '@0@.desktop'.format(app_id),
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: datadir / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

# Install icons
install_subdir(
  'data/icons',
  install_dir: datadir,
)


# Install launcher script
conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('pkgdatadir', pkgdatadir)
conf.set('localedir', prefix / get_option('localedir'))

configure_file(
  input: 'bin/{{ NEW_NAME }}.in',
  output: '{{ NEW_NAME }}',
  configuration: conf,
  install: true,
  install_dir: bindir,
  install_mode: 'rwxr-xr-x',
)


appstream_file = i18n.merge_file(
        input: 'data/{{ ID_NAME }}.metainfo.xml.in',
       output: '{{ ID_NAME }}.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: datadir / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

install_data('data/{{ ID_NAME }}.gschema.xml',
  install_dir: datadir / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])


subdir('po')

# Post-install script
gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
