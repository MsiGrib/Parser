using OsuParsers.Enums.Replays;

namespace DiffTimeOSU
{
    internal class Print
    {
        private const int lenghtLine = 20;

        // ReplayFrame
        public void printStandardKeys(List<StandardKeys> standardKeys)
        {
            int i = 0;
            int count = 0;
            Console.WriteLine("---------------------StandardKeys-------------------------------------------");
            foreach (StandardKeys item in standardKeys)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
                count++;
            }
            Console.WriteLine($"\n-Count: {count}------------------------------------------------------------");
        }

        public void printTaikoKeys(List<TaikoKeys> taikoKeys)
        {
            int i = 0;
            Console.WriteLine("--------------------TaikoKeys-----------------------------------------------");
            foreach (TaikoKeys item in taikoKeys)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
            }
            Console.WriteLine("\n---------------------------------------------------------------------------");
        }

        public void printCatchKeys(List<CatchKeys> catchKeys)
        {
            int i = 0;
            Console.WriteLine("---------------------CatchKeys-----------------------------------------------");
            foreach (CatchKeys item in catchKeys)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
            }
            Console.WriteLine("\n---------------------------------------------------------------------------");
        }

        public void printManiaKeys(List<ManiaKeys> maniaKeys)
        {
            int i = 0;
            Console.WriteLine("-----------------------ManiaKeys---------------------------------------------");
            foreach (ManiaKeys item in maniaKeys)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
            }
            Console.WriteLine("\n---------------------------------------------------------------------------");
        }

        public void printTimeDiff(List<int> timeDiff)
        {
            int i = 0;
            Console.WriteLine("-----------------------TimeDiff----------------------------------------------");
            foreach (int item in timeDiff)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
            }
            Console.WriteLine("\n---------------------------------------------------------------------------");
        }

        public void printTime(List<int> time)
        {
            int i = 0;
            int count = 0;
            Console.WriteLine("-----------------------Time--------------------------------------------------");
            foreach (int item in time)
            {
                Console.Write(item.ToString() + " ");
                if (i == lenghtLine / 2)
                {
                    Console.WriteLine();
                    i = 0;
                    continue;
                }
                i++;
                count++;
            }
            Console.WriteLine($"\n-Count: {count}------------------------------------------------------------");
        }
    }
}
