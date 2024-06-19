import open3d as o3d
import numpy as np

ply = o3d.io.read_point_cloud('/home/cheng/slam_bag/dlo_map.pcd')

o3d.visualization.draw_geometries([ply])