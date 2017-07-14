import pymel.core as pmc

def generate_stripes():
    """
    Generate stripes emulating the works of Alberto Biasi
    (https://www.google.com/search?q=alberto+biasi&tbm=isch)
    
    The stripes start from a parametric curve, pass through
    a set of shapes and end in another parametric curve.
    
    The user must have selected the root of a hierarchy tree with this shape:
    root
      |- Starting curve
      |- Ending curve
      |- Nails
          |- Row 1
          |  |- Nail 1.1
          |  |- Nail 1.2
          |  | ...
          |  |- Nail 1.N
          |- Row 2
          |  |- Nail 2.1
          |  |- Nail 2.2
          |  | ...
          |  |- Nail 2.N
          | ...
          |- Row M
             |- Nail M.1
             |- Nail M.2
             | ...
             |- Nail M.N
    Where the "nails" are the shapes where the stripes must pass through.
    If the hierarchy shape is correct, there will be N nails for row (so N stripes)
    and M rows.
    To work properly, the nails must have their longest side aligned with the world y-axis.
    
    The function creates N nurbsSurfaces (called "stripe1", "stripe2", ..., "stripeN"),
    groups them under a node called "stripes", sets "stripes" as a child of the root of
    the selected hierarchy and returns the "stripes" group.
    """
    
    def gen_fn(upper):
        def internal(bbox):
            xmin, ymin, zmin, xmax, ymax, zmax = bbox
            pt = pmc.datatypes.VectorN([
                (xmin + xmax)/2,
                ymax if upper else ymin,
                (zmin + zmax)/2])
            return pt
        return internal
    
    
    tree = pmc.ls(sl=True)[0]
    children = tree.getChildren()
    splints = [node for node in children if len(node.getShapes()) > 0]
    nail_rows = [child for child in children if child not in splints][0].getChildren()
    
    # n represents how many stripes will be generated. It cannot be 0
    n = len(nail_rows[0].getChildren())
    if n == 0: raise ValueError
    
    # Get the NURBS curves
    cA, cB = [s.getShape() for s in splints]
    
    inv_n = 1./n
    param_pts = [(e+i)*inv_n for i in range(n) for e in [0,1]]
    
    fns = [gen_fn(True), gen_fn(False)]
    int_pts = []
    for row in nail_rows:
        bboxes = [pmc.exactWorldBoundingBox(child) for child in row.getChildren()]
        int_pts += [[fn(bbox) for bbox in bboxes for fn in fns]]
    
    curves = []
    for i in range(2*n):
        strip = []
        strip.append(cA.getPointAtParam(param_pts[i], space='world'))
        for row in int_pts:
            strip.append(row[i])
        strip.append(cB.getPointAtParam(param_pts[i], space='world'))
        curves.append(pmc.curve(d=1,p=strip))
        
    g = pmc.group(p=tree, n='stripes')
    for i in range(n):
        cs = curves[2*i:2*i+2]
        g.addChild(pmc.loft(cs, n='stripe{0}'.format(i+1))[0])
        pmc.delete(cs)
        
    return g
