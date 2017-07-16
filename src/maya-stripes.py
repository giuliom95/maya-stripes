# pySampleDGNode.py

import sys

import maya.api.OpenMaya as OpenMaya


def maya_useNewAPI():
    pass


##########################################################
# Plug-in 
##########################################################
class stripeNode(OpenMaya.MPxNode):
    nodeName = 'stripe'
    nodeClassify = 'general'
    nodeId = OpenMaya.MTypeId(0x1923)

    startCurveAttr = OpenMaya.MObject()
    endCurveAttr = OpenMaya.MObject()

    startCurveStartAttr = OpenMaya.MObject()
    startCurveEndAttr = OpenMaya.MObject()
    endCurveStartAttr = OpenMaya.MObject()
    endCurveEndAttr = OpenMaya.MObject()

    surfaceOutAttr = OpenMaya.MObject()

    @staticmethod
    def creator():
        return stripeNode()

    @staticmethod
    def initializer():
        numericAttrFn = OpenMaya.MFnNumericAttribute()
        typedAttrFn = OpenMaya.MFnTypedAttribute()

        #==================================
        # INPUT NODE ATTRIBUTE(S)
        #==================================

        stripeNode.startCurveAttr = typedAttrFn.create('startCurve', 'sc', OpenMaya.MFnNurbsCurveData.kNurbsCurve)
        stripeNode.endCurveAttr = typedAttrFn.create('endCurve', 'ec', OpenMaya.MFnNurbsCurveData.kNurbsCurve)
        typedAttrFn.readable = False
        typedAttrFn.writable = True
        typedAttrFn.storable = False
        typedAttrFn.hidden = False
        stripeNode.addAttribute(stripeNode.startCurveAttr)
        stripeNode.addAttribute(stripeNode.endCurveAttr)

        stripeNode.startCurveStartAttr = numericAttrFn.create('startCurveStartParam', 'ssp', OpenMaya.MFnNumericData.kFloat, 0.0)
        stripeNode.startCurveEndAttr = numericAttrFn.create('startCurveEndParam', 'sep', OpenMaya.MFnNumericData.kFloat, 1.0)
        stripeNode.endCurveStartAttr = numericAttrFn.create('endCurveStartParam', 'esp', OpenMaya.MFnNumericData.kFloat, 0.0)
        stripeNode.endCurveEndAttr = numericAttrFn.create('endCurveEndParam', 'eep', OpenMaya.MFnNumericData.kFloat, 1.0)
        typedAttrFn.readable = False
        typedAttrFn.writable = True
        typedAttrFn.storable = True
        typedAttrFn.hidden = False
        stripeNode.addAttribute(stripeNode.startCurveStartAttr)
        stripeNode.addAttribute(stripeNode.startCurveEndAttr)
        stripeNode.addAttribute(stripeNode.endCurveStartAttr)
        stripeNode.addAttribute(stripeNode.endCurveEndAttr)

        #==================================
        # OUTPUT NODE ATTRIBUTE(S)
        #==================================
        stripeNode.surfaceOutAttr = typedAttrFn.create('surface', 'out', OpenMaya.MFnNurbsCurveData.kNurbsSurface)
        typedAttrFn.storable = False
        typedAttrFn.writable = False
        typedAttrFn.readable = True
        typedAttrFn.hidden = False
        stripeNode.addAttribute(stripeNode.surfaceOutAttr)

        #==================================
        # NODE ATTRIBUTE DEPENDENCIES
        #==================================
        stripeNode.attributeAffects(stripeNode.startCurveAttr, stripeNode.surfaceOutAttr)
        stripeNode.attributeAffects(stripeNode.endCurveAttr, stripeNode.surfaceOutAttr)
        stripeNode.attributeAffects(stripeNode.startCurveStartAttr, stripeNode.surfaceOutAttr)
        stripeNode.attributeAffects(stripeNode.startCurveEndAttr, stripeNode.surfaceOutAttr)
        stripeNode.attributeAffects(stripeNode.endCurveStartAttr, stripeNode.surfaceOutAttr)
        stripeNode.attributeAffects(stripeNode.endCurveEndAttr, stripeNode.surfaceOutAttr)

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    def compute(self, pPlug, pDataBlock):
        if(pPlug == stripeNode.surfaceOutAttr):
            outSurfaceDataHandle = pDataBlock.outputValue(stripeNode.surfaceOutAttr)

            curveDataHandle = pDataBlock.inputValue(stripeNode.startCurveAttr)

            curve = OpenMaya.MFnNurbsCurve(curveDataHandle.asNurbsCurve())

            print '====1===='
            outSurfaceFn = OpenMaya.MFnNurbsSurface()
            cvs = [[-4, 0, 1], [-4, 0, -1], [4, 1, 0], [4, -1, 0]]
            outSurface = outSurfaceFn.create(cvs, [0, 1], [0, 1], 1, 1, outSurfaceFn.kOpen, outSurfaceFn.kOpen, False)
            print outSurfaceFn.area()
            print '====2===='
            #outSurfaceDataHandle.setMObject(outSurface)
            #outSurfaceDataHandle.setClean()

        else:
            return OpenMaya.kUnknownParameter


##########################################################
# Plug-in initialization.
##########################################################
def initializePlugin(mobject):
    ''' Initialize the plug-in '''
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerNode(
            stripeNode.nodeName,
            stripeNode.nodeId,
            stripeNode.creator,
            stripeNode.initializer,
            OpenMaya.MPxNode.kDependNode,
            stripeNode.nodeClassify)
    except:
        sys.stderr.write('Failed to register node: ' + stripeNode.nodeName)
        raise


def uninitializePlugin(mobject):
    ''' Uninitializes the plug-in '''
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(stripeNode.nodeId)
    except:
        sys.stderr.write('Failed to deregister node: ' + stripeNode.nodeName)
        raise
