using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.IO;

public class Client
{
    private const int CLIENT_TYPE = 2;
    private Stream stream;

    public Client()
    {
        var tcp = new TcpClient("localhost", 7777);
        stream = tcp.GetStream();

        var type = System.BitConverter.GetBytes(CLIENT_TYPE);

        stream.Write(type, 0, sizeof(byte));
    }

    public void SendImage(Texture2D image)
    {
        var bytes = image.EncodeToJPG();
        stream.Write(bytes, 0, bytes.Length);
    }

    private IEnumerator SendPic()
    {
        yield return null;

        byte[] image = File.ReadAllBytes(Application.dataPath + "/Images/rasp_pi.jpg");
        stream.Write(image, 0, image.Length);

        //yield return new WaitForSeconds(1f);

        stream.Write(image, 0, image.Length);
        stream.Close();
    }
}
