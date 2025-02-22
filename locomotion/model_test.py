import genesis as gs
import numpy as np
import time
gs.init(backend=gs.vulkan)

scene = gs.Scene(
    show_viewer = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True,
        world_frame_size = 1.0,
        show_link_frame  = False,
        show_cameras     = False,
        plane_reflection = True,
        ambient_light    = (0.1, 0.1, 0.1),
    ),
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.URDF(file="assets/urdf/nz2/urdf/nz2.urdf",
    pos=(0.0, 0.0, 0.15)
    ),
    # gs.morphs.MJCF(file="assets/mjcf/nz/nz.xml",
    # pos=(0.0, 0.0, 0.265)
    # ),
    # vis_mode='collision'
)

cam = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 2.5),
    lookat = (0, 0, 0.5),
    fov    = 30,
    GUI    = False,
)
scene.build()

jnt_names = [
    # "left_hip_joint",
    "left_thigh_joint",
    "left_calf_joint",
    # "right_hip_joint",
    "right_thigh_joint",
    "right_calf_joint",
    "left_wheel_joint",
    "right_wheel_joint",
]
dofs_idx = [franka.get_joint(name).dof_idx_local for name in jnt_names]
franka.set_dofs_kp(
    kp = np.array([20,20,20,20,40,40]),
    dofs_idx_local = dofs_idx,
)
franka.set_dofs_kv(
    kv = np.array([0.5,0.5,0.5,0.5,0.5,0.5]),
    dofs_idx_local = dofs_idx,
)
left_knee = franka.get_joint("left_calf_joint")



# 渲染rgb、深度、分割掩码和法线图
# rgb, depth, segmentation, normal = cam.render(rgb=True, depth=True, segmentation=True, normal=True)

# cam.start_recording()
import numpy as np

while True:
    franka.control_dofs_position(
            np.array([0.0, 0.0, 0.0, 0.0, 10.0, 10.0]),
            dofs_idx,
        )
    scene.step()
    # print(franka.get_pos())
    # left_knee_pos = left_knee.get_pos()
    # print("left_knee_pos    ",left_knee_pos)
    # force = franka.get_links_net_contact_force()
    # dof_vel = franka.get_dofs_velocity()
    # print("dof_vel:",dof_vel)
    # time.sleep(0.1)
    cam.render()
# cam.stop_recording(save_to_filename='video.mp4', fps=60)