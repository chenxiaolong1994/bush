xml_content_starting = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE stax SYSTEM "stax.dtd">
<stax>
	<defaultcall function="func_test"/>
	<function name="func_test">
        <sequence>
'''

xml_content = '''            <loop from="0" to="0">
                <testcase name="'{case.name}'">
                    <sequence>
                        <stafcmd>
                            <location>'local'</location>
                            <service>'event'</service>
                            <request>'generate type monitor subtype properties property status=running property case_name={case.name} property task_name={task_name}'</request>
                        </stafcmd>
                        <process>
                            <location>'local'</location>
                            <command>'{case.command}'</command>
                            <parms>'{script_path}/{case.script} {case.param}'</parms>
                        </process>
                        <if expr="RC == 0">
                            <tcstatus result="'pass'"/>
                            <else>
                                <tcstatus result="'fail'"/>
                            </else>
                        </if>
                        <stafcmd>
                            <location>'local'</location>
                            <service>'event'</service>
                            <request>'generate type monitor subtype properties property status=finish property case_name={case.name} property task_name={task_name}'</request>
                        </stafcmd>
                    </sequence>
                </testcase>
            </loop>
'''

xml_content_ending = '''        <loop from="0" to="0">
                <testcase name="'last_case'">
                    <sequence>
                        <stafcmd>
                            <location>'local'</location>
                            <service>'event'</service>
                            <request>'generate type monitor subtype endoftest'</request>
                        </stafcmd>
                        <tcstatus result="'pass'"/>
                    </sequence>
                </testcase>
            </loop>
        </sequence>
    </function>
</stax>
'''

import re
import os
from django.conf import settings

tmp_handle_global = None


def generate_xml(task_name, task_cases):
    proj_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(proj_name, 'media/script')
    xml_path = settings.MEDIA_ROOT + settings.CASE_DIR
    xml_name = '.'.join([task_name, 'xml'])
    # cases = Suite.objects.get(id=p_suite).case_set.all()
    xml_location = os.path.join(xml_path, xml_name)
    print xml_location

    if os.path.exists(xml_location):
        os.remove(xml_location)
    with open(xml_location, 'a+') as xml_handle:
        xml_handle.write(xml_content_starting)
        for task_case in task_cases:
            xml_content_towrite = xml_content.format(case=task_case.case, script_path=script_path, task_name=task_name)
            xml_handle.write(xml_content_towrite)
        xml_handle.write(xml_content_ending)
