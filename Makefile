all: bom

bom:
	xsltproc -o "sds_tool/sds_tool-bom.csv" \
	    "/Applications/Kicad/kicad.app/Contents/SharedSupport/plugins/bom_with_title_block_2_csv.xsl" \
	    "sds_tool/sds_tool.xml"
