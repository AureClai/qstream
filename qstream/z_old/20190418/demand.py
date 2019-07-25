#Loop over the links """
try:
    nodesLayer = QgsProject.instance().mapLayersByName("Noeuds")[0]
    linksLayer = QgsProject.instance().mapLayersByName("Liens")[0]
except IndexError:
    print("No link layer...")

with edit(nodesLayer):
    features = nodesLayer.selectedFeatures()
    if features:
        delIDs = []
        for feature in features:
            delIDs.append(feature.id())
        # delete the features
        #nodesLayer.deleteFeatures(delIDs)

with edit(nodesLayer):
    for nodeID in delIDs:
        # Catch the links with that node in up_node
        expr = QgsExpression( "\"up_node\"='{}'".format( id ) )
        features = linksLayer.getFeatures( QgsFeatureRequest( expr ) )
        for feature in features:

    
