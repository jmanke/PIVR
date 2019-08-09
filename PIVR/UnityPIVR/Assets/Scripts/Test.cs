using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Test : MonoBehaviour
{
    public void Start()
    {
        var test = new C();
        Debug.Log(test.PrintName());
    }
}

public class A
{
    public virtual string PrintName() { return "A"; }
} 

public class B : A
{
    public override string PrintName()
    {
        return $"{base.PrintName()}B";
    }
}

public class C : B
{
    public override string PrintName()
    {
        return $"{base.PrintName()}C";
    }
}

