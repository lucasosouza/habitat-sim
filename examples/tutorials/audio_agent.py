# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import habitat_sim
# import habitat_sim.sim
# import habitat_sim.sensor
# import habitat_sim._ext.habitat_sim_bindings as hsim_bindings

import numpy as np
from numpy import ndarray
import quaternion as qt

from datetime import datetime

def printTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def main():
    backend_cfg = habitat_sim.SimulatorConfiguration()
    backend_cfg.scene_id = (
        "data/scene_datasets/mp3d_example/17DRP5sb8fy/17DRP5sb8fy.glb"
    )
    backend_cfg.scene_dataset_config_file = ("data/scene_datasets/mp3d_example/17DRP5sb8fy/scene_dataset_config.json")
    backend_cfg.enable_physics = True

    agent_config = habitat_sim.AgentConfiguration()

    cfg = habitat_sim.Configuration(backend_cfg, [agent_config])

    sim = habitat_sim.Simulator(cfg)

    # create the acoustic configs
    acoustics_config = hsim_bindings.HabitatAcousticsConfiguration()
    acoustics_config.dumpWaveFiles = True
    acoustics_config.enableMaterials = True

    # create channel layout
    channel_layout = hsim_bindings.HabitatAcousticsChannelLayout()
    channel_layout.channelType = 3
    channel_layout.channelCount = 2

    # create the Audio sensor specs
    audio_sensor_spec = habitat_sim.AudioSensorSpec()
    audio_sensor_spec.uuid = "audio_sensor"
    audio_sensor_spec.outputFolderPath = "/home/sangarg/AudioSimulation"
    audio_sensor_spec.acousticsConfig = acoustics_config
    audio_sensor_spec.channelLayout = channel_layout

    # add the audio sensor
    sim.add_sensor(audio_sensor_spec)

    # Get the audio sensor object
    audio_sensor = sim.get_agent(0)._sensors["audio_sensor"]

    # # set habitat acoustic configs
    # audio_sensor.setAudioSimulationConfigs(acoustics_config)

    # # optionally set the output folder path
    # outputFolderPath = "/home/sangarg/AudioSimulation"
    # audio_sensor.setOutputFolder(outputFolderPath)

    # set audio source location, no need to set the agent location, will be set implicitly
    audio_sensor.setAudioSourceTransform(np.array([3.1035, 1.57245, -4.15972]), np.array([1.0, 0.0, 0.0, 0.0]))

    # run the simulation
    for i in range (1):
        print(i)
        print("Start Time : ")
        printTime()
        p = outputFolderPath + str(i) + "/ir";
        obs = sim.get_sensor_observations()
        print (obs)
        # # get the simulation results
        # channelCount = audio_sensor.getChannelCount()
        # sampleCount = audio_sensor.getSampleCount()

        # for channelIndex in range (0, channelCount):
        #     filePath = p + str(channelIndex) + ".txt"
        #     f = open(filePath, "w")
        #     print("Writing file : ", filePath)
        #     for sampleIndex in range (0, sampleCount):
        #         f.write(str(sampleIndex) + "\t" + str(audio_sensor.getImpulseResponse(channelIndex, sampleIndex)) + "\n")
        #     f.close()

        print("End Time : ")
        printTime()

    sim.close()

if __name__ == "__main__":
    main()
