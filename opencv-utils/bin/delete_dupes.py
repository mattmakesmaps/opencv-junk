import argparse
import os
import sys

def get_abs_path(in_path):
    """
    Given a relative or absolute path, return the absolute path.
    :param in_path:
    :return:
    """
    if os.path.isabs(in_path):
        return in_path
    else:
        return os.path.abspath(in_path)

if __name__ == '__main__':
    # Define command line interface
    parser = argparse.ArgumentParser(description='Given a source and target directory, '
                                                 'if files are present in the source, delete from the target.')

    parser.add_argument('source_path', help="Path containing source files.", action="store")
    parser.add_argument('target_path', help="Path containing files to delete if they appear in source.", action="store")
    parser.add_argument('--dry-run', help="Don't delete, just output files marked for delete.",
                         action="store_true", default=False)
    args = parser.parse_args()
    full_source_path = get_abs_path(args.source_path)
    full_target_path = get_abs_path(args.target_path)

    source_files = os.listdir(full_source_path)
    target_files = os.listdir(full_target_path)

    if args.dry_run:
        sys.stdout.write("DRY RUN: NO FILES WILL BE DELETED\n")
    else:
        sys.stdout.write("WARNING: THE FOLLOWING FILES WILL BE DELETED\n")

    for source_file in source_files:
        if source_file in target_files:
            target_file = os.path.join(full_target_path, source_file)
            sys.stdout.write("%s\n" % target_file)
            # Real Run, Delete Files
            if not args.dry_run:
                os.remove(target_file)
