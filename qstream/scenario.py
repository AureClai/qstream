import os
import numpy as np
import matplotlib.pyplot as plt

import json

from osgeo import ogr

class Scenario:
    def __init__(self, file):
        if os.path.isfile(file):
            print("Loading the file : " + file + '...')
            self.sourcePath = file
            self.__source = ogr.Open(file)
        else:
            print("No such file")
            print(file)
        self.__scenario = {}
        self.__load()

    def __load(self):
        scenario = {}
        # ROAD Types
        layer = self.__source.GetLayerByName("RoadTypes")
        scenario.update({"RoadTypes" : self.__getDict(layer, {'name' : 'name', 'speed' : 'speed', 'capacity' : 'capacity', 'jam_density' : 'jam_density'})})
        # Nodes
        layer = self.__source.GetLayerByName("Noeuds")
        scenario.update({"Nodes" : self.__getDict(layer, {'name' : 'name', 'type' : 'Type'})})
        # Links
        layer = self.__source.GetLayerByName("Liens")
        scenario.update({"Links" : self.__getDict(layer, {'name' : 'name', 'priority' : 'Priority', 'num_lanes' : 'NumLanes', 'up_node' : 'NodeUpID', 'down_node' : 'NodeDownID', 'road_type' : 'road_type', 'capacity' : 'Capacity', 'speed' : 'Speed'})})
        # Vehicle Types
        layer = self.__source.GetLayerByName("VehicleTypes")
        scenario.update({"VehicleClass" : self.__getDict(layer, {'name' : 'Name'})})
        # Periods
        layer = self.__source.GetLayerByName("Periods")
        scenario.update({"Periods" : self.__getDict(layer, {'start' : 'start'})})
        # Demand
        scenario.update({"Demand" : self.__getDemand()})
        # Assign Road types parameters to links
        scenario.update({"Links" : self.__updateDFLinks(scenario["Links"], scenario["RoadTypes"])})
        # Assign downstream and upstream to nodes
        scenario.update({"Nodes" : self.__updateNodesInOut(scenario["Links"], scenario["Nodes"])})
        # get the lengths of the links
        scenario.update({"Links" : self.__updateLinksLength(scenario["Links"])})
        # get the points of the links
        scenario.update({"Links" : self.__updateLinksPoints(scenario["Links"])})
        # get the Entries
        scenario.update({"Entries" : self.__getEntries(scenario["Nodes"])})
        # get the exits
        scenario.update({"Exits" : self.__getExits(scenario["Nodes"])})
        # get the General variables
        scenario.update({"General" : self.__getGeneral()})
        # get the Regulations variables
        scenario.update({"Regulations" : self.__getRegulations()})

        self.__scenario = scenario

    def __getDict(self, layer, dictFields):
        dict = {}
        for feature in layer:
            feat = {}
            for field in dictFields:
                feat.update({dictFields[field] : feature.GetField(field)})
            dict.update({feature.GetFID() : feat})
        return dict

    def __getDemand(self):
        # Get layer of demand
        layer = self.__source.GetLayerByName("Demand")
        # Store each Feature data in one array
        data = []
        for feature in layer:
            data.append([feature.GetField('period'), feature.GetField('vehicle_type'), feature.GetField('origin'), feature.GetField('destination'), feature.GetField('flow')])
        data = np.array(data, dtype = float)
        return data

    def __updateDFLinks(self, links, roadTypes):

        for link in links:
            if links[link]['Capacity']!=None:
                links[link]['Capacity'] /= 3600
            if links[link]['Speed']!=None:
                links[link]['Speed'] /= 3.6
            DF = {}
            roadType = links[link]["road_type"]
            if not roadType:
                roadType = 1 #si vide
            DF.update({'u' : roadTypes[roadType]['speed']/3.6,
                       'C' : roadTypes[roadType]['capacity']/3600,
                       'kx' : roadTypes[roadType]['jam_density']/1000
                       })
            DF["w"] = DF["C"] /(DF["kx"] - DF["C"] /DF["u"])
            links[link].update({"FD" : DF})
        return links

    def __updateNodesInOut(self, links, nodes):
        # Get the array of links in and outs
        table = np.zeros([len(links), 3], dtype=int)
        count = 0
        for link in links:
            table[count,0] = link
            table[count,1] = links[link]["NodeUpID"]
            table[count,2] = links[link]["NodeDownID"]
            count = count + 1

        for node in nodes:
            upLinks = table[list(np.where(table[:,2]==node)[0]), 0]
            downLinks = table[list(np.where(table[:,1]==node)[0]), 0]
            nodes[node].update({'OutgoingLinksID' : downLinks, 'IncomingLinksID' : upLinks, 'NumOutgoingLinks' : len(downLinks), 'NumIncomingLinks' : len(upLinks)})
        return nodes

    def __updateLinksLength(self, links):
        layer = self.__source.GetLayerByName("Liens")
        # loop over all the features
        for feature in layer:
            # get the geometry of the feature
            geom = feature.GetGeometryRef()
            # update the length
            links[feature.GetFID()].update({"Length" : geom.Length()})
        return links

    def __updateLinksPoints(self, links):
        layer = self.__source.GetLayerByName("Liens")
        # Loop over all the features
        for feature in layer:
            # Get the geometry of the feature
            geom = feature.GetGeometryRef()
            # loop over the lines
            Xs = []
            Ys = []
            for line in geom:
                #loop over the points
                for point in line.GetPoints():
                    Xs.append(point[0])
                    Ys.append(point[1])
            # Compute the array of points
            points = np.vstack((np.array(Xs), np.array(Ys)))
            links[feature.GetFID()].update({"Points" : points})
        return links

    def __getEntries(self, nodes):
        entries = {}
        for node in list(nodes.keys()):
            if nodes[node]["Type"]==1:
                entries.update({node : {}})
        return entries

    def __getExits(self, nodes):
        exits = {}
        for node in list(nodes.keys()):
            if nodes[node]["Type"]==2:
                exits.update({node : {}})
        return exits

# Get the general variable from the Genral layeri in the gpkg
# 1. Simulation Start
# 2. Simulation End
# 3. TimeStep
# 4. ActiveUpStreamCapacity
    def __getGeneral(self):
        # get the layer
        layer = self.__source.GetLayerByName("General")
        # initialization of the variable
        General = {}
        General["SimulationDuration"] = [0,0]
        for feat in layer:
            if feat.GetFID() == 1:
                General["SimulationDuration"][0] = float(feat["value"])
            elif feat.GetFID() == 2:
                General["SimulationDuration"][1] = float(feat["value"])
            elif feat.GetFID() == 4:
                General["ActiveUpStreamCapacity"] = bool(int(feat["value"]))

        return General

    def __getRegulations(self):
        # get the layer
        Regulations = {}
        layer = self.__source.GetLayerByName("Regulations")
        # initialization of the variable

        if layer == None:
            return Regulations

        for feat in layer:
            reg = {}
            reg["Type"] = feat["Type"]
            reg["Args"] = json.loads(feat["Arguments"])
            Regulations.update({feat.GetFID() : reg})

        return Regulations

###############################################################################

    def getAsDict(self):
        return self.__scenario

    def __plotLink(self,feature, ax, color='black', linewidth = 0.5):
        geom = feature.GetGeometryRef()
        xmin = np.inf
        xmax = -np.inf
        ymin = np.inf
        ymax = -np.inf
        firstPoint = []
        lastPoint = []
        for line in geom:
            Xs = []
            Ys = []
            for point in line.GetPoints():
                Xs.append(point[0])
                Ys.append(point[1])
                if not firstPoint:
                    firstPoint.extend([point[0], point[1]])
                if point[0] < xmin:
                    xmin = point[0]
                if point[0] > xmax:
                    xmax = point[0]
                if point[1] < ymin:
                    ymin = point[1]
                if point[1] > ymax:
                    ymax = point[1]
            ax.plot(Xs, Ys, linewidth = linewidth, color=color)
        lastPoint.extend([point[0], point[1]])
        return (xmin, xmax, ymin, ymax, firstPoint, lastPoint)

    def plotScenario(self,axes):
        XGmin = np.inf
        XGmax = -np.inf
        YGmin = np.inf
        YGmax = -np.inf
        # Get the layer of links
        layer = self.__source.GetLayerByName("Liens")
        for feature in layer:
            xmin, xmax, ymin, ymax, _, _ = self.__plotLink(feature, axes)
            if xmin < XGmin:
                XGmin = xmin
            if xmax > XGmax:
                XGmax = xmax
            if ymin < YGmin:
                YGmin = ymin
            if ymax > YGmax:
                YGmax = ymax
        axes.set_xlim(XGmin, XGmax)
        axes.set_ylim(YGmin, YGmax)

    def __plotRoute(self,route,axes):
        # Get the layer of links
        layer = self.__source.GetLayerByName("Liens")
        fp = []
        for fid in route["Path"]:
            feature = layer.GetFeature(fid)
            xmin, xmax, ymin, ymax, FP, lp = self.__plotLink(feature, axes, color = 'orange', linewidth = 3)
            if not fp:
                fp = FP
        axes.plot(fp[0], fp[1], marker='+', ms = 20, color='green')
        axes.plot(lp[0], lp[1], marker='+', ms= 20,color='red')

    def makeImageRoute(self, route):
        fig = plt.figure(figsize = [12.8,9.6])
        ax = fig.add_subplot(111)
        self.plotScenario(ax)
        self.__plotRoute(route, axes = ax)
        ax.set_title("Shortest Path\nfrom Entry " + str(route["EntryID"]) + " to Exit " + str(route["ExitID"]))
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        plt.grid(True)

        return fig

    def saveAsNpy(self, name="Export"):
        fullname = name + ".npy"
        np.save(fullname, self.__scenario)
        return fullname
