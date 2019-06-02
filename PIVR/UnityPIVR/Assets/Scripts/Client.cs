using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.IO;

public class Client : MonoBehaviour
{
    private const int CLIENT_TYPE = 2;
    private Stream stream;

    private void Start()
    {
        var tcp = new TcpClient("localhost", 7777);
        stream = tcp.GetStream();

        var type = System.BitConverter.GetBytes(CLIENT_TYPE);

        stream.Write(type, 0, sizeof(byte));

        StartCoroutine(SendPic());
    }

    private IEnumerator SendPic()
    {
        yield return null;

        byte[] image = File.ReadAllBytes(Application.dataPath + "/Images/rasp_pi.jpg");
        stream.Write(image, 0, image.Length);
        stream.Close();
    }
}
