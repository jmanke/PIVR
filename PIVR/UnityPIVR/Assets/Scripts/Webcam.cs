using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Webcam : MonoBehaviour
{
    public RawImage rawimage;
    public int deviceIndex = 0;

    void Start()
    {
        var devices = WebCamTexture.devices;

        foreach (var device in devices)
        {
            Debug.Log(device.name);
        }

        var webcamTexture = new WebCamTexture(devices[deviceIndex].name);
        rawimage.texture = webcamTexture;

        Debug.Log("Resolution = " + rawimage.texture.width + ", " + rawimage.texture.height);

        rawimage.material.mainTexture = webcamTexture;
        webcamTexture.Play();
    }
}
