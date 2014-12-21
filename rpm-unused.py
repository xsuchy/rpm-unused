#!/usr/bin/python3
# vim: noai:ts=4:sw=4:expandtab
import datetime
import humanize
import os
import rpm

def get_last_used(package_header):
    package_files = package_header.fiFromHeader()
    last_time = 0
    ff = ""
    for f in package_files:
        filename = f[0]
        try:
            atime = os.stat(filename).st_atime
        except FileNotFoundError:
            continue
        if atime > last_time:
            last_time = atime
            ff = filename
    #print(ff)
    return last_time

def main():
    packages = []
    ts = rpm.TransactionSet()
    packages = [ts.dbMatch()]
    sorted_packages = []
    # pylint: enable=no-member
    for mi in packages:
        for package_hdr in mi:
            last_used = get_last_used(package_hdr)
            if last_used == 0:
                # no files in package
                continue
            package_name = "{0}-{1}-{2}".format(package_hdr['name'].decode('utf-8'), package_hdr['version'].decode('utf-8'), package_hdr['release'].decode('utf-8'))
            sorted_packages.append([package_name, last_used, package_hdr['size']])
            #print("{0} {1}".format(package_name, last_used))
    sorted_packages.sort(key=lambda x: x[1], reverse=True)

    print("{0:20} {1}".format("package name", "last time used"))
    for (package_name, last_used, size) in sorted_packages:
        print("{0:20} {1} {2}".format(package_name, datetime.datetime.fromtimestamp(last_used).strftime("%Y-%m-%d"), humanize.naturalsize(size, binary=True)))



try:
    main()
except BrokenPipeError:
    pass
