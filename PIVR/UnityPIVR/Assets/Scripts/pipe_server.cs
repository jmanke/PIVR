using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.IO.Pipes;
using System.Threading;

public class pipe_server : MonoBehaviour
{
	// Use this for initialization
	void Start ()
    {
        //StartCoroutine(Test());
    }

    private IEnumerator Test()
    {
        yield return null;

        // Open the named pipe.
        var server = new NamedPipeServerStream("PIVR", PipeDirection.InOut);

        Debug.Log("Waiting for connection...");
        server.WaitForConnection();

        Debug.Log("Connected.");
        var br = new BinaryReader(server);
        var bw = new BinaryWriter(server);
        var test = new byte[1];

        yield return null;

        while (true)
        {
            try
            {
                string str = "";

                while (true)
                {
                    if (server.Read(test, 0, 1) < 1)
                    {
                        Debug.Log("Nothing");
                        break;
                    }
                    else
                    {
                        Debug.Log("Something is in the stream");
                        server.Flush();
                        break;
                    }
                    //var b = br.ReadByte();

                    //if (b < 1)
                    //    break;

                    //char c = Convert.ToChar(b);
                    //str += c;
                }

                br = new BinaryReader(server);
                if (str.Length > 0)
                    Debug.Log("Got a message: " + str);

                //Debug.Log("Got here 1");
                //var len = (int)br.ReadUInt32();            // Read string length
                //Debug.Log("Got here 2");
                //var str = new string(br.ReadChars(len));    // Read string
                //Debug.Log("Got here 3");

                //Debug.Log($"Read: \"{str}\"");

                //var buf = System.Text.Encoding.ASCII.GetBytes(str);     // Get ASCII byte array     
                //bw.Write((uint)buf.Length);                // Write string length
                //bw.Write(buf);                              // Write string
                //Debug.Log($"Wrote: \"{str}\"");
            }
            catch (EndOfStreamException)
            {
                break;                    // When client disconnects
            }

            yield return null;
        }

        Console.WriteLine("Client disconnected.");
        server.Close();
        server.Dispose();
    }
}
