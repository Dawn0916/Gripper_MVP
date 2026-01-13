import pybullet as p
import pybullet_data

def setup_world(dt: float, gui: bool = True) -> int:
    cid = p.connect(p.GUI if gui else p.DIRECT)
    # Hide the side camera previews / GUI overlays
    p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
    p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
    p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
    # Hide other UI
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)          # hides most of the UI

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setTimeStep(dt)
    p.setGravity(0, 0, -9.81)

    # Optional: make contact more stable
    p.setPhysicsEngineParameter(numSolverIterations=200)

    p.loadURDF("plane.urdf") # load a ground plane
    return cid 

def set_camera(target=(0.5, 0.0, 0.1), distance=0.35, yaw=45, pitch=-25):
    p.resetDebugVisualizerCamera(
        cameraDistance=distance,
        cameraYaw=yaw,
        cameraPitch=pitch,
        cameraTargetPosition=list(target),
    )

def spawn_box_object(
    pos=(0.56, 0.0, 0.10),
    half_extents=(0.015, 0.02, 0.03),
    mass=0.05,
) -> int:
    """
    Box center at pos. Box full size is 2*half_extents.
    """
    col = p.createCollisionShape(p.GEOM_BOX, halfExtents=list(half_extents)) # Creates collision geometry for physics contact.
    vis = p.createVisualShape(p.GEOM_BOX, halfExtents=list(half_extents), rgbaColor=[0.9, 0.9, 0.9, 1.0]) # Create visual geometry for rendering.

    # Create a rigid body with mass, collision shape, visual shape, and initial position.
    obj = p.createMultiBody( 
        baseMass=mass,
        baseCollisionShapeIndex=col,
        baseVisualShapeIndex=vis,
        basePosition=list(pos),
    )

    # Set friction to reduce slipping during pinch
    p.changeDynamics(obj, -1, lateralFriction=1.2, spinningFriction=0.001, rollingFriction=0.001)
    return obj



