#-*- coding: utf-8 -*-

import codecs
import getopt
import io
import os
import sys

class LineCounter:
    def __init__(self):
        self.SetPath(os.getcwd())
        self.SetResultFile("lines.txt")
        self.SetSuffixs("c,cpp,h,hpp,py")
        self.SetNameOnly(False)

    def CountLine(self):
        output = io.StringIO()

        self.__Output(self.__CountLine(self.__path), 0, 0, output)

        outputfile = open(self.__filename, "w")
        outputfile.writelines(output.getvalue())
        outputfile.close()

        output.close()
        print("The result stores in '" + self.__filename + "'.")

    def SetPath(self, path):
        self.__path = os.path.abspath(path)

    def SetResultFile(self, filename):
        self.__filename = filename

    def SetSuffixs(self, suffixline):
        self.__emptysuffix = False
        self.__ignoresuffix = False
        self.__suffixs = ()
        words = suffixline.split(",")
        if "*" in words:
            self.__ignoresuffix = True
            return
        suffixwords = set()
        for word in words:
            if word == "":
                self.__emptysuffix = True
            else:
                suffixwords.add("." + word)
        self.__suffixs = tuple(suffixwords)

    def SetNameOnly(self, nameonly):
        self.__nameonly = nameonly

    def PrintUsage(self):
        print("options:")
        print("    -p path: default value is cur dir")
        print("    -s suffixs: default value is 'c,cpp,h,hpp,py'")
        print("    -r filename: default value is 'lines.txt'")
        print("    -n yes|no: show name only, default 'no'")
        print("    --help: print this usage")

    def __CheckSuffix(self, path):
        if self.__ignoresuffix:
            return True
        elif self.__emptysuffix and not "." in os.path.basename(path):
            return True
        else:
            return path.endswith(self.__suffixs)

    def __CountLine(self, path):
        count = 0
        basename = os.path.basename(path)
        if os.path.isdir(path):
            filelist = []
            for child in os.listdir(path):
                childpath = os.path.join(path, child)
                node = self.__CountLine(childpath)
                if node is not None:
                    filelist.append(node)
                    (_,c,_) = node
                    count += c
            if len(filelist) > 0:
                return (basename, count, filelist)
            else:
                return None
        elif self.__CheckSuffix(path):
            for line in codecs.open(path, "r", "utf-8", "ignore"):
                count += 1
            return (basename, count, [])
        else:
            return None
        
    def __Output(self, node, indent, dirlen, output):
        if node is None:
            return;

        (name, count, subnodes) = node
        if count <= 0 and not self.__nameonly:
            return

        output.write(indent * " " + "+" + dirlen * "-" + name)
        if not self.__nameonly:
            output.write(": " + str(count))
        output.write(os.linesep)
        
        for subnode in subnodes:
            self.__Output(subnode, indent + dirlen, len(name), output)

if __name__ == "__main__":
    counter = LineCounter()
    opts, args = getopt.getopt(sys.argv[1:], "s:p:r:n:", ["help"])
    for op, value in opts:
        if op == "-s":
            counter.SetSuffixs(value)
        if op == "-p":
            counter.SetPath(value)
        if op == "-r":
            counter.SetResultFile(value)
        if op == "-n":
            counter.SetNameOnly(value == "yes")
        if op == "--help":
            counter.PrintUsage()
            sys.exit()

    print("'linecounter --help' for help")
    counter.CountLine()
