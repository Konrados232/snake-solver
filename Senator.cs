using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace colab_proj
{
    internal class Senator
    {

        public string Name { get; private set; }

        public Senator()
        {
            Name = "Armstrong";
        }

        public Senator(string name)
        {
            Name = name;
        }

    }
}
