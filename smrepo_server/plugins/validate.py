import fnmatch
from .archive import get_archive_paths


# Yak's SMRepo Source Archive Structure
# See https://github.com/theY4Kman/smrepo-server/wiki/Source-Archive-Structure
STRUCTURE = {
    'addons': {
        'sourcemod': {
            'configs': {
                '<plug-in name>': { '!masks': ('*.cfg', '*.ini', '*.txt') },
                '!masks': ('<plug-in name>.cfg', '<plug-in name>.ini', '<plug-in name>.txt'),
                '!blacklist': ('admin_groups.cfg', 'admin_levels.cfg', 'admin_overrides.cfg', 'adminmenu_cfgs.txt',
                               'adminmenu_custom.txt', 'adminmenu_grouping.txt', 'adminmenu_sorting.txt',
                               'admins_simple.ini', 'admins.cfg', 'core.cfg', 'databases.cfg',
                               'languages.cfg', 'maplists.cfg', 'plugin_settings.cfg',
                               # Folders
                               'geoip', 'sql-init-scripts')
            },
            'scripting': {
                'include': { '!masks': ('<plug-in name>.inc',) },
                '<plug-in name>': { '!masks': ('*.sp',) },

                '!masks': ('<plug-in name>.sp',),
                '!blacklist': ('admin-sql-prefetch.sp', 'admin-sql-threaded.sp', 'adminhelp.sp', 'adminmenu.sp',
                               'antiflood.sp', 'basebans.sp', 'basechat.sp', 'basecomm.sp', 'basecommands.sp',
                               'basetriggers.sp', 'basevotes.sp', 'clientprefs.sp', 'funcommands.sp', 'funvotes.sp',
                               'mapchooser.sp', 'nextmap.sp', 'nominations.sp', 'playercommands.sp', 'randomcycle.sp',
                               'reservedslots.sp', 'rockthevote.sp', 'sounds.sp', 'sql-admin-manager.sp',
                               # Folders
                               'admin-flatfile', 'adminmenu', 'basebans', 'basecomm', 'basecommands', 'basevotes',
                               'funcommands', 'funvotes', 'playercommands', 'testsuite')
            },
            'translations': {
                '<plug-in name>': { '!masks': ('<plug-in name>.phrases.txt',) },
                '!blacklist': lambda name: len(name) > 3
            }
        }
    },
    'cfg': {
        'sourcemod': {
            '!masks': ('<plug-in name>.cfg',),
            '!blacklist': ('sm_warmode_off.cfg', 'sm_warmode_on.cfg', 'sourcemod.cfg')
        }
    }
}

def validate_archive(filename, plugin_name):
    """Takes a ZipFile/TarFile-like object and validates it against the structure defined above. Returns True if the
    archive is valid, otherwise a list of tuples (path, error_msg) for every invalid path in the archive.
    """
    errors = []
    for path in get_archive_paths(filename):
        cur = STRUCTURE
        for part in filter(lambda d: d != '.', path.split('/')):
            if part in cur:
                cur = cur[part]
                continue

            # Throw out any hidden paths (that begin with a period)
            if part.startswith('.'):
                break

            # Error out if the path is in the blacklist
            blacklist = cur.get('!blacklist')
            if callable(blacklist) and blacklist(part, path):
                errors.append((path, 'Blacklisted path'))
                break

            try:
                for black in blacklist:
                    if part.lower() == black.lower():
                        errors.append((path, 'Blacklisted path'))
                        break
            except TypeError:
                pass

            # Check the whitelisting masks now
            matched = False
            for mask in cur.get('!masks', ()):
                iterations = (mask,)
                if '<plug-in name>' in mask:
                    iterations = (mask.replace('<plug-in name>', plugin_name),
                                  mask.replace('<plug-in name>', 'plugin.%s' % plugin_name))
                for mask in iterations:
                    if fnmatch.fnmatch(part, mask):
                        matched = True
                        break
            
            if matched:
                break

            errors.append((path, 'Invalid path'))

    if errors:
        return errors
    return True

