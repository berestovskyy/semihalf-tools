from StcPython import StcPython
import time

######### CONFIGURATION #########
# Filename of XML file exported from Spirent TestCenter GUI
xml_filename = 'untitled.xml'
# Port locations (from GUI)
port1_location = '//10.2.100.6/1/1'
port2_location = '//10.2.100.6/1/2'
# Results dir name
results_dir = 'untitled-results'
#################################

# All possible generator, analyzer, rxstreamsummary port result attributes:
generator_attributes='totalframecount totaloctetcount generatorframecount generatoroctetcount generatorsigframecount generatorundersizeframecount generatoroversizeframecount generatorjumboframecount totalframerate totaloctetrate generatorframerate generatoroctetrate generatorsigframerate generatorundersizeframerate generatoroversizeframerate generatorjumboframerate generatorcrcerrorframecount generatorl3checksumerrorcount generatorl4checksumerrorcount generatorcrcerrorframerate generatorl3checksumerrorrate generatorl4checksumerrorrate totalipv4framecount totalipv6framecount totalmplsframecount generatoripv4framecount generatoripv6framecount generatorvlanframecount generatormplsframecount totalipv4framerate totalipv6framerate totalmplsframerate generatoripv4framerate generatoripv6framerate generatorvlanframerate generatormplsframerate totalbitrate generatorbitrate l1bitcount l1bitrate pfcframecount pfcpri0framecount pfcpri1framecount pfcpri2framecount pfcpri3framecount pfcpri4framecount pfcpri5framecount pfcpri6framecount pfcpri7framecount l1bitratepercent'

analyzer_attributes='totalframecount totaloctetcount sigframecount undersizeframecount oversizeframecount jumboframecount minframelength maxframelength pauseframecount totalframerate totaloctetrate sigframerate undersizeframerate oversizeframerate jumboframerate pauseframerate fcserrorframecount ipv4checksumerrorcount tcpchecksumerrorcount udpchecksumerrorcount prbsfilloctetcount prbsbiterrorcount fcserrorframerate ipv4checksumerrorrate tcpchecksumerrorrate udpchecksumerrorrate prbsfilloctetrate prbsbiterrorrate ipv4framecount ipv6framecount ipv6overipv4framecount tcpframecount udpframecount mplsframecount icmpframecount vlanframecount ipv4framerate ipv6framerate ipv6overipv4framerate tcpframerate udpframerate mplsframerate icmpframerate vlanframerate trigger1count trigger1rate trigger2count trigger2rate trigger3count trigger3rate trigger4count trigger4rate trigger5count trigger5rate trigger6count trigger6rate trigger7count trigger7rate trigger8count trigger8rate combotriggercount combotriggerrate totalbitrate prbsbiterrorratio vlanframerate l1bitcount l1bitrate pfcframecount fcoeframecount pfcframerate fcoeframerate pfcpri0framecount pfcpri1framecount pfcpri2framecount pfcpri3framecount pfcpri4framecount pfcpri5framecount pfcpri6framecount pfcpri7framecount pfcpri0quanta pfcpri1quanta pfcpri2quanta pfcpri3quanta pfcpri4quanta pfcpri5quanta pfcpri6quanta pfcpri7quanta prbserrorframecount prbserrorframerate userdefinedframecount1 userdefinedframerate1 userdefinedframecount2 userdefinedframerate2 userdefinedframecount3 userdefinedframerate3 userdefinedframecount4 userdefinedframerate4 userdefinedframecount5 userdefinedframerate5 userdefinedframecount6 userdefinedframerate6 l1bitratepercent outseqframecount preambletotalbytes preambleminlength preamblemaxlength droppedframecount inorderframecount reorderedframecount duplicateframecount lateframecount firstarrivaltime lastarrivaltime'

rxstreamsummaryresults_attributes='avginterarrivaltime avgjitter avglatency bitcount bitrate cellcount cellrate comp16_1 comp16_2 comp16_3 comp16_4 comp32 countertimestamp droppedframecount droppedframepercent droppedframepercentrate droppedframerate duplicateframecount duplicateframerate expectedseqnum fcserrorframecount fcserrorframerate firstarrivaltime framecount framerate histbin10count histbin10name histbin10rate histbin11count histbin11name histbin11rate histbin12count histbin12name histbin12rate histbin13count histbin13name histbin13rate histbin14count histbin14name histbin14rate histbin15count histbin15name histbin15rate histbin16count histbin16name histbin16rate histbin1count histbin1name histbin1rate histbin2count histbin2name histbin2rate histbin3count histbin3name histbin3rate histbin4count histbin4name histbin4rate histbin5count histbin5name histbin5rate histbin6count histbin6name histbin6rate histbin7count histbin7name histbin7rate histbin8count histbin8name histbin8rate histbin9count histbin9name histbin9rate inorderframecount inorderframerate inseqframecount inseqframerate ipv4checksumerrorcount ipv4checksumerrorrate l1bitcount l1bitrate lastarrivaltime lastseqnum lateframecount lateframerate maxframelength maxinterarrivaltime maxjitter maxlatency minframelength mininterarrivaltime minjitter minlatency octetcount octetrate outseqframecount outseqframerate portstrayframes prbsbiterrorcount prbsbiterrorrate prbsbiterrorratio prbserrorframecount prbserrorframerate prbsfilloctetcount prbsfilloctetrate reorderedframecount reorderedframerate rfc4689absoluteavgjitter rxport seqrunlength shorttermavginterarrivaltime shorttermavgjitter shorttermavglatency sigframecount sigframerate streamindex tcpudpchecksumerrorcount tcpudpchecksumerrorrate totalinterarrivaltime totaljitter totaljitterrate totallatency'
#################################


# Create Spirent API instance
stc = StcPython()
# Create project - the root object
hProject = stc.create("project")
# Print WARN and ERROR messages
stc.config("automationoptions", logTo='stdout', logLevel='WARN')

# Load configuration from XML
stc.perform('loadfromxml', filename=xml_filename)
# Search for objects of type 'Port' in the configuration and extract them
rv = stc.perform('GetObjects', ClassName='Port', Condition='IsVirtual=false')
ports = str.split(rv['ObjectList'])
if len(ports) != 2:
	print("Error: failed to find two ports in configuration\n")
	exit(1)

# Configure ports, set results dir, set sequencer to stop on error
stc.config(ports[0], location=port1_location)
stc.config(ports[1], location=port2_location)
stc.config(hProject + '.testResultSetting', saveResultsRelativeTo='NONE', resultsDirectory=results_dir)
stc.config('system1.sequencer', errorHandler='STOP_ON_ERROR')

# Connect to chassis and try to reserve and map the ports. Set RevokeOwner to TRUE to
# kick out the other user (takes a minute)
rv = stc.perform('attachPorts', RevokeOwner='FALSE')
if not rv:
	print("Error: Failed to reserve ports - exiting..\n")
	exit(1)

# Apply configuration (verify and upload to chassis)
stc.apply()

# Subscribe to test results. Configured attributes will be saved to .csv results file every 1 second of
# the test. Possible fields in viewAttributeList are listed in API docs: 'RxStreamSummaryResults.htm'. 
# Results may be viewed in .csv file or you may browse the SQL .db file directly. 
# Best way to view them is via Results API object.
rx_dataset = stc.subscribe(parent=hProject, resultParent=hProject, configType='StreamBlock', resultType='RxStreamSummaryResults', viewAttributeList='framerate' , interval='1', filenamePrefix='RxStreamSummaryResults')

# Subscribe to generator and analyzer results
generator_dataset = stc.subscribe(parent=hProject, resultParent=hProject, configType='generator', resultType='generatorportresults', filterList='', viewAttributeList='totalframecount generatorframecount totalframerate generatorframerate totalbitrate generatorbitrate', interval='1', filenamePrefix='generatorportresults')
analyzer_dataset = stc.subscribe(parent=hProject, resultParent=hProject, configType='analyzer', resultType='analyzerportresults', filterList='', viewAttributeList='totalframecount totalframerate totalbitrate', interval='1', filenamePrefix='analyzerportresults')

# If sequencer is configured in XML, start it and wait for it to finish
#stc.perform('sequencerStart')
#rv = stc.waitUntilComplete()  # this call is blocking. check rv for pass/fail

# Start generators without using sequencer
print("Starting generators\n")
generator1 = stc.get(ports[0], 'children-Generator')
generator2 = stc.get(ports[1], 'children-Generator')
stc.perform('GeneratorStart', GeneratorList=generator1)
stc.perform('GeneratorStart', GeneratorList=generator2)

print("Wait 10 seconds..\n")
time.sleep(10)

# Check frames per second
sb1 = stc.get(ports[0], 'children-StreamBlock')
rx_results1 = stc.get(sb1, 'children-RxStreamSummaryResults')
framerate1 = stc.get(rx_results1, 'FrameRate')
sb2 = stc.get(ports[1], 'children-StreamBlock')
rx_results2 = stc.get(sb2, 'children-RxStreamSummaryResults')
framerate2 = stc.get(rx_results2, 'FrameRate')

# Get analyzer results (unused)
analyzer1 = stc.get(ports[0], 'children-Analyzer')
analyzer_results1 = stc.get(analyzer1, 'children-AnalyzerPortResults')
analyzer2 = stc.get(ports[1], 'children-Analyzer')
analyzer_results2 = stc.get(analyzer2, 'children-AnalyzerPortResults')

# Stop generators
stc.perform('GeneratorStop', GeneratorList=generator1)
stc.perform('GeneratorStop', GeneratorList=generator2)
print("Generators stopped\n")
print("Port1 framerate: " + framerate1 + ", Port2 framerate: " + framerate2 + "\n")

# Disconnect from chassis, release ports and reset the config in chassis
print("Disconnecting from chassis\n")
stc.perform('chassisDisconnectAll')
stc.perform('resetConfig')
