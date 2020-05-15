#Iterate through watchtowers
watchtowers=($(seq -w 101 104))
for idx in ${!watchtowers[*]}
do

    printf "Setting up watchtower%s.. " ${watchtowers[$idx]}
    docker -H watchtower${watchtowers[$idx]}.local run -it --rm -d -v /data:/data --name run_localization --net=host duckietown/dt-core:daffy-hatteland-edit-localization-arm32v7
    docker -H watchtower${watchtowers[$idx]}.local run --rm --name acquisition-bridge --network=host -e ROBOT_TYPE=watchtower -e LAB_ROS_MASTER_IP=192.168.1.216 -dit duckietown/acquisition-bridge:daffy-hatteland-edit-localization-arm32v7
    
done

autobots=($(seq -w 27 27))
for idx in ${!autobots[*]}
do

    printf "Setting up autobot%s.. " ${autobots[$idx]}
    docker -H autobot${autobots[$idx]}.local run --rm --name acquisition-bridge --network=host -e ROBOT_TYPE=watchtower -e LAB_ROS_MASTER_IP=192.168.1.216 -dit duckietown/acquisition-bridge:daffy-hatteland-edit-localization-arm32v7
    dts duckiebot demo --demo_name all_drivers --duckiebot_name autobot${autobots[$idx]} --package_name duckiebot_interface --image duckietown/dt-duckiebot-interface:daffy
    dts duckiebot demo --demo_name all --duckiebot_name autobot${autobots[$idx]} --package_name car_interface --image duckietown/dt-car-interface:daffy
    dts duckiebot demo --demo_name lane_following --duckiebot_name autobot${autobots[$idx]} --package_name duckietown_demos --image duckietown/dt-core:daffy
    dts duckiebot keyboard_control autobot${autobots[$idx]} --base_image duckietown/dt-core:daffy-amd64
    docker run --name odometry_processor_${autobots[$idx]} --network=host -dit --rm  -e ACQ_ROS_MASTER_URI_SERVER_IP=192.168.1.216 -e ACQ_DEVICE_NAME=autobot${autobots[$idx]} duckietown/wheel-odometry-processor:daffy-amd64

done