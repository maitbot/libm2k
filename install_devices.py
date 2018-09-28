#!/usr/bin/env python

import os

pluginList = []

for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".ini")]:
	if "devices" in dirpath:
        	#print os.path.join(dirpath, filename)
		f = open(os.path.join(dirpath, filename))
		line = f.readline().strip()
		pluginList.append(line[1:len(line) - 1])

installed_devices = ""

installed_devices += """
#ifndef INSTALLED_DEVICES_H
#define INSTALLED_DEVICES_H

#include <map>
#include <string>

#include "libm2k/genericdevice.hpp"

// generated includes for plugins

"""
for plugin in pluginList:
	installed_devices += ("""#include "devices/{0}/{1}.hpp"\n""").format(plugin, plugin.lower())



installed_devices += """
using namespace libm2k::devices;

enum DeviceTypes {
"""

for plugin in pluginList:
	installed_devices += ("""\tDev{0},\n""").format(plugin)

installed_devices += """
	Other
};
"""

installed_devices += """
typedef std::map<std::string, DeviceTypes> device_name_to_type_map;

device_name_to_type_map dev_map = {
"""
for i in range(len(pluginList)):
	if i != len(pluginList) - 1:
		installed_devices += (""" {{"{0}", DeviceTypes::Dev{0}}},\n""").format(pluginList[i])
	else:
		installed_devices += (""" {{"{0}", DeviceTypes::Dev{0}}}""").format(pluginList[i])
installed_devices += """
};
"""
installed_devices += """
DeviceTypes get_type_from_name(std::string name)
{
	DeviceTypes t = DeviceTypes::Other;
	try {
		t = dev_map.at(name);
		return t;
	} catch (std::out_of_range e){

	}
	return t;
}
"""

installed_devices += """
GenericDevice* buildDevice(std::string name) // enum Device Name
{
	DeviceTypes t = get_type_from_name(name);
	switch (t) {
"""

for plugin in pluginList:
	installed_devices += ("""//case Dev{0}: return new {0}();""").format(plugin)

installed_devices += """
	case Other: return new GenericDevice("");
	}
}

#endif // INSTALLED_DEVICES_H
"""

print installed_devices
