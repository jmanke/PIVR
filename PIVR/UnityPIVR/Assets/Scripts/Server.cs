using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.IO.Pipes;

/* TYPES
 * 1: Request Baseline Image
 * 2: 
 * 
 * */

public class Server
{
    public bool alive;
    private CaptureDevice cd;
    public byte[] testImg;
    NamedPipeServerStream stream;
    private bool pendingWrite = false;

    public Server(CaptureDevice cd)
    {
        this.cd = cd;
    }

    public void Start()
    {
        alive = true;

        try
        {
            stream = new NamedPipeServerStream("PIVR_pipe", PipeDirection.InOut);
        } 
        catch (Exception e)
        {
            Debug.LogError(e.ToString());
            stream = null;
            return;
        }

        Debug.Log("Waiting for connection...");
        stream.WaitForConnection();
        Debug.Log("Connected.");

        while (alive)
        {
            byte[] typeBuf = new byte[sizeof(byte)];
            byte[] sizeBuf = new byte[sizeof(int)];
            stream.Read(typeBuf, 0, sizeof(byte));
            stream.Read(sizeBuf, 0, sizeof(Int32));
            int dataSize = BitConverter.ToInt32(sizeBuf, 0);
            var dataBuf = new byte[dataSize];
            stream.Read(dataBuf, 0, dataSize);

            // Client disconnected
            if (dataSize < 1)
            {
                // When client disconnects
                Debug.Log("Client disconnected");
                break;
            }

            ProcessMessage(typeBuf[0], dataSize, dataBuf);

            while (pendingWrite){ }

            stream.Flush();
            stream.WaitForPipeDrain();
            
        }

        Debug.Log("Thread terminated");
        stream.Close();
        stream.Dispose();
    }

    private void GetBaselineImage(object args)
    {
        var img = cd.TakeScreenshot();
        byte[] bytes = img.EncodeToJPG();
        stream.Write(bytes, 0, bytes.Length);
        pendingWrite = false;
        Debug.Log("Sent baseline img");
    }

    private void GetBestFitImage(object args)
    {
        Debug.Log("Position model");
        var kpPairs = args as List<Tuple<Vector2, Vector2>>;
        cd.PositionModel(kpPairs);
        var bestFit = cd.TakeScreenshot();
        byte[] bytes = bestFit.EncodeToJPG();
        Debug.Log("Sending best fit...");
        stream.Write(bytes, 0, bytes.Length);
        Debug.Log("Sent best fit");
        pendingWrite = false;
        cd.ResetModel();
    }

    private void ProcessMessage(byte type, int size, byte[] data)
    {
        Debug.Log($"Type: {type}, size: {size}");

        switch (type)
        {
            // Request for baseline image
            case 1:
                Debug.Log("Request baseline img");
                pendingWrite = true;
                MainThread.Instance.QueueEvent(GetBaselineImage, null);
                break;
            // Request for image at pixel values
            case 2:
                Debug.Log("Request for best fit image");
                var kpPairs = new List<Tuple<Vector2, Vector2>>();

                for (int i = 0; i < size; i += sizeof(float) * 4)
                {
                    pendingWrite = true;

                    float x1 = BitConverter.ToSingle(data, i);
                    float y1 = BitConverter.ToSingle(data, i + sizeof(float));
                    float x2 = BitConverter.ToSingle(data, i + sizeof(float) * 2);
                    float y2 = BitConverter.ToSingle(data, i + sizeof(float) * 3);
                    var coord1 = new Vector2(x1, y1);
                    var coord2 = new Vector2(x2, y2);

                    kpPairs.Add(new Tuple<Vector2, Vector2>(coord1, coord2));
                }

                string msg = "";

                foreach (var pair in kpPairs)
                {
                    msg += pair.ToString() + ", ";
                }

                Debug.Log(msg);
                MainThread.Instance.QueueEvent(GetBestFitImage, kpPairs);
                break;
        }
    }
}
