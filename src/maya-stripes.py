# pySampleDGNode.py

import sys

import maya.api.OpenMaya as OpenMaya
import pymel.core as pmc


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

    bboxMinAttr = OpenMaya.MObject()
    bboxMaxAttr = OpenMaya.MObject()
    bboxMatrixAttr = OpenMaya.MObject()
    nailsAttr = OpenMaya.MObject()

    surfaceOutAttr = OpenMaya.MObject()

    @staticmethod
    def creator():
        return stripeNode()

    @staticmethod
    def initializer():
        numericAttrFn = OpenMaya.MFnNumericAttribute()
        typedAttrFn = OpenMaya.MFnTypedAttribute()
        compoundAttrFn = OpenMaya.MFnCompoundAttribute()
        matrixAttrFn = OpenMaya.MFnMatrixAttribute()

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

        stripeNode.bboxMinAttr = numericAttrFn.createPoint('bboxMin', 'bmi')
        stripeNode.bboxMaxAttr = numericAttrFn.createPoint('bboxMax', 'bma')
        stripeNode.bboxMatrixAttr = matrixAttrFn.create('worldMatrix', 'wm', OpenMaya.MFnMatrixAttribute.kFloat)
        stripeNode.nailsAttr = compoundAttrFn.create('nails', 'n')
        compoundAttrFn.readable = False
        compoundAttrFn.writable = True
        compoundAttrFn.storable = False
        compoundAttrFn.hidden = False
        compoundAttrFn.array = True
        compoundAttrFn.addChild(stripeNode.bboxMinAttr)
        compoundAttrFn.addChild(stripeNode.bboxMaxAttr)
        compoundAttrFn.addChild(stripeNode.bboxMatrixAttr)
        stripeNode.addAttribute(stripeNode.nailsAttr)

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
        stripeNode.attributeAffects(stripeNode.nailsAttr, stripeNode.surfaceOutAttr)

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    def compute(self, pPlug, pDataBlock):
        if(pPlug == stripeNode.surfaceOutAttr):
            outSurfaceDataHandle = pDataBlock.outputValue(stripeNode.surfaceOutAttr)

            startCurveDataHandle = pDataBlock.inputValue(stripeNode.startCurveAttr)
            endCurveDataHandle = pDataBlock.inputValue(stripeNode.endCurveAttr)

            startCurve = OpenMaya.MFnNurbsCurve(startCurveDataHandle.asNurbsCurve())
            endCurve = OpenMaya.MFnNurbsCurve(endCurveDataHandle.asNurbsCurve())

            attrs = [
                stripeNode.startCurveStartAttr,
                stripeNode.startCurveEndAttr,
                stripeNode.endCurveStartAttr,
                stripeNode.endCurveEndAttr]

            handles = [pDataBlock.inputValue(x) for x in attrs]
            params = [h.asFloat() for h in handles]

            points = [startCurve.getPointAtParam(p, OpenMaya.MSpace.kWorld) for p in params[0:2]]
            knotsU = [0]

            nailsArrayDataHandle = pDataBlock.inputArrayValue(stripeNode.nailsAttr)
            while not nailsArrayDataHandle.isDone():
                nailDataHandle = nailsArrayDataHandle.inputValue()

                matrix = nailDataHandle.child(stripeNode.bboxMatrixAttr).asFloatMatrix()
                minVector = nailDataHandle.child(stripeNode.bboxMinAttr).asFloatVector()
                maxVector = nailDataHandle.child(stripeNode.bboxMaxAttr).asFloatVector()

                minP = OpenMaya.MFloatPoint(minVector)*matrix
                maxP = OpenMaya.MFloatPoint(maxVector)*matrix

                xz = [.5*(minP.x + maxP.x), .5*(minP.z + maxP.z)]
                points += [[xz[0], minP.y, xz[1]]]
                points += [[xz[0], maxP.y, xz[1]]]
                knotsU += [knotsU[-1] + 1]

                nailsArrayDataHandle.next()

            points += [endCurve.getPointAtParam(p, OpenMaya.MSpace.kWorld) for p in params[2:4]]
            knotsU += [knotsU[-1] + 1]

            dataCreator = OpenMaya.MFnNurbsSurfaceData()
            outData = dataCreator.create()
            outSurfaceFn = OpenMaya.MFnNurbsSurface()
            outSurface = outSurfaceFn.create(points, knotsU, [0, 1], 1, 1, outSurfaceFn.kOpen, outSurfaceFn.kOpen, False, parent=outData)

            outSurfaceDataHandle.setMObject(outData)
            pDataBlock.setClean(pPlug)

        else:
            return OpenMaya.kUnknownParameter


class DoSripesCommand(OpenMaya.MPxCommand):
    commandName = 'doStripes'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def commandCreator():
        return DoSripesCommand()

    def doIt(self, args):
        try:
            root = pmc.ls(sl=True)[0]
        except:
            raise RuntimeError('Plese select a hierarchy')

        curvesTrans = [c for c in root.getChildren() if c.getShapes() != []]
        try:
            startCurve, endCurve = [c.getShape() for c in curvesTrans]
        except:
            raise RuntimeError('There must be exactly two curves in the hierarchy')

        nailsRoot = [c for c in root.getChildren() if c.getShapes() == []][0]
        nailRows = nailsRoot.getChildren()

        if len(nailRows) == 0:
            raise RuntimeError('There must be at least one nail row')

        stripesNumbers = [len(r.getChildren()) for r in nailRows]
        stripesNum = stripesNumbers[0]
        if stripesNum == 0:
            raise RuntimeError('There must be at least one nail per stripe')
        if not all([s == stripesNum for s in stripesNumbers]):
            raise RuntimeError('Evey nail row must have the same number of nails')

        surfaces = []

        scKnotDomain = startCurve.getKnotDomain()
        ecKnotDomain = endCurve.getKnotDomain()
        scDelta = (scKnotDomain[1] - scKnotDomain[0]) / stripesNum
        ecDelta = (ecKnotDomain[1] - ecKnotDomain[0]) / stripesNum

        for i in range(stripesNum):
            stripeNode = pmc.createNode('stripe', n='stripeCreator')
            pmc.connectAttr(startCurve.attr('worldSpace[-1]'), stripeNode.attr('startCurve'))
            pmc.connectAttr(endCurve.attr('worldSpace[-1]'), stripeNode.attr('endCurve'))

            for j,row in enumerate(nailRows):
                nail = row.childAtIndex(i).getShape()
                pmc.connectAttr(nail.attr('boundingBox.boundingBoxMin'), stripeNode.attr('nails[{0}].bboxMin'.format(j)))
                pmc.connectAttr(nail.attr('boundingBox.boundingBoxMax'), stripeNode.attr('nails[{0}].bboxMax'.format(j)))
                pmc.connectAttr(nail.attr('worldMatrix[-1]'), stripeNode.attr('nails[{0}].worldMatrix'.format(j)))

            stripeNode.setAttr('startCurveStartParam', scDelta*i)
            stripeNode.setAttr('startCurveEndParam', scDelta*(i+1))
            stripeNode.setAttr('endCurveStartParam', ecDelta*i)
            stripeNode.setAttr('endCurveEndParam', ecDelta*(i+1))

            transformNode = pmc.createNode('transform', p=root, n='stripe1')
            surfaceNode = pmc.createNode('nurbsSurface', p=transformNode)

            # This line throws a warning
            pmc.connectAttr(stripeNode.attr('surface'), surfaceNode.attr('create'))

            surfaces += [transformNode]

        pmc.select(surfaces)
        pmc.group(n='stripes')
        pmc.hyperShade(assign='lambert1')


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

    try:
        mplugin.registerCommand(
            DoSripesCommand.commandName,
            DoSripesCommand.commandCreator
        )
    except:
        sys.stderr.write(
            'Failed to register command: ' + DoSripesCommand.commandName)
        raise


def uninitializePlugin(mobject):
    ''' Uninitializes the plug-in '''
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(stripeNode.nodeId)
    except:
        sys.stderr.write('Failed to deregister node: ' + stripeNode.nodeName)
        raise

    try:
        mplugin.deregisterCommand(DoSripesCommand.commandName)
    except:
        sys.stderr.write('Failed to unregister command: ' + DoSripesCommand.commandName)
        raise
