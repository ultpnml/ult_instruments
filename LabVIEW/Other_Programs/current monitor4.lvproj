﻿<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="10008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="current monitor4.vi" Type="VI" URL="../current monitor4.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="current monitor4" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{864A793C-4961-451D-9034-77D8781BAD9B}</Property>
				<Property Name="App_INI_GUID" Type="Str">{8D0BF8DC-9CCC-4F8A-A07D-FB97FA153555}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">current monitor4</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/current monitor4/current monitor4</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Destination[0].destName" Type="Str">Application.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/current monitor4/Application.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/current monitor4/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{A4DDB54C-478D-4E4B-9D74-0A5D6C7D7708}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/current monitor4.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fileDescription" Type="Str">current monitor4</Property>
				<Property Name="TgtF_fileVersion.major" Type="Int">1</Property>
				<Property Name="TgtF_internalName" Type="Str">current monitor4</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2020 </Property>
				<Property Name="TgtF_productName" Type="Str">current monitor4</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{AC294495-BC00-4E20-97F8-56E26905F15D}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Application.exe</Property>
			</Item>
		</Item>
	</Item>
</Project>
