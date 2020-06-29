#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    __commands = {
        "create",
        "show",
        "destroy",
        "all",
        "update",
        "count"
    }

    def precmd(self, line):
        """
        Method executed just before the command line line is interpreted,
        but after the input prompt is generated and issued
        """
        new_line = ""
        if len(line) > 0:
            s_line = line.strip()
            l_dots = s_line.split(".")
            if len(l_dots) >= 2:
                l_parentesis = l_dots[1].split("(")
                if len(l_parentesis) >= 2:
                    cls_name = l_dots[0]
                    command = l_parentesis[0]
                    if command in self.__commands:
                        # Ojo aqui depronto hay que agregar:
                        # and l_dots[0] in self.__classes
                        new_line = "{} {}".format(command, cls_name)
                        if l_parentesis[1] == ")":
                            return new_line
                        elif s_line[-1] == ")":
                            parentesis_idx = s_line.index('(')
                            arguments = s_line[parentesis_idx + 1: -1]
                            try:
                                args = eval(arguments)
                                argu_str = arguments[1:-1]
                                argu_tup = "({})".format(arguments.
                                                         replace("\"", "'"))
                                if type(args) is str and args != argu_str:
                                    raise Exception
                                if type(args) is tuple and \
                                        str(args) != argu_tup:
                                    raise Exception
                            except:
                                return line
                            if type(args) is str \
                                    and command != "all"\
                                    and command != "create"\
                                    and command != "count":
                                uid = args
                                new_line += " '{}'".format(uid)
                                return new_line
                            elif type(args) is tuple and command == "update":
                                if len(args) == 3 and type(args[0]) is str\
                                        and type(args[1]) is str:
                                    new_line += " '{}' '{}' ".format(args[0],
                                                                     args[1])
                                    if type(args[2]) == str:
                                        new_line += "'{}'".format(args[2])
                                    else:
                                        new_line += "{}".format(args[2])
                                    return new_line
                                if len(args) == 2 and type(args[0]) is str\
                                        and type(args[1]) == dict\
                                        and len(args[1]):
                                        u_id = "{} '{}'".format(cls_name,
                                                                args[0])
                                        for k, v in args[1].items():
                                            if type(v) is str:
                                                u_cmd = "{} '{}' '{}'"\
                                                    .format(u_id, k, v)
                                            else:
                                                u_cmd = "{} '{}' {}"\
                                                    .format(u_id, k, v)
                                            self.do_update(u_cmd)
                                        return ""
        return line

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """
        Exits the program
        """
        print()
        return True

    def emptyline(self):
        """
        Executes anything
        """
        pass

    def help_quit(self):
        """Quit command help"""
        print("Quit command to exit the program\n")

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves
        it (to the JSON file) and prints the id
        """
        if not len(arg) > 0:
            print("** class name missing **")
        else:
            arguments = arg.split()
            if arguments[0] in self.__classes:
                new_obj = eval(arguments[0])()
                storage.save()
                print(new_obj.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        """
        if len(arg) == 0:
            print("** class name missing **")
        else:
            arguments = shlex.split(arg)
            if arguments[0] not in self.__classes:
                print("** class doesn't exist **")
            else:
                if len(arguments) >= 2:
                    objects = storage.all()
                    key = "{}.{}".format(arguments[0], arguments[1])
                    if key in objects:
                        print(objects[key])
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        """
        if len(arg) == 0:
            print("** class name missing **")
        else:
            arguments = shlex.split(arg)
            if arguments[0] not in self.__classes:
                print("** class doesn't exist **")
            else:
                if len(arguments) >= 2:
                    objects = storage.all()
                    key = "{}.{}".format(arguments[0], arguments[1])
                    if key in objects:
                        objects.pop(key)
                        storage.save()
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        """
        output = []
        objects = storage.all()
        if len(arg) == 0:
            for obj in objects.values():
                output.append(obj.__str__())
            print(output)
        else:
            arguments = shlex.split(arg)
            if (arguments[0] in self.__classes):
                for obj in objects.values():
                    if arguments[0] == obj.__class__.__name__:
                        output.append(obj.__str__())
                print(output)
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        if len(arg) == 0:
            print("** class name missing **")
            return False
        objects = storage.all()
        # arguments = shlex.split(arg)
        arguments = shlex.split(arg)
        if arguments[0] not in self.__classes:
            print("** class doesn't exist **")
            return False
        if len(arguments) == 1:
            print("** instance id missing **")
            return False
        key = "{}.{}".format(arguments[0], arguments[1])
        if key not in objects:
            print("** no instance found **")
            return False
        if len(arguments) == 2:
            print("** attribute name missing **")
            return False
        if len(arguments) == 3:
            print("** value missing **")
            return False
        if len(arguments) >= 4:
            obj = objects[key]
            if hasattr(obj, arguments[2]):
                value_type = type(getattr(obj, arguments[2]))
                setattr(obj, arguments[2], value_type(arguments[3]))
            else:
                val_str = "'{}'".format(arguments[3])
                if val_str == arg.strip()[-len(val_str):].replace("\"", "'"):
                    setattr(obj, arguments[2], arguments[3])
                else:
                    try:
                        real_val = eval(arguments[3])
                        setattr(obj, arguments[2], real_val)
                    except:
                        print("** value missing **")
                        return False
                # setattr(obj, arguments[2], arguments[3])
            storage.save()

    def do_count(self, arg):
        """
        Retrieves the number of instances of a class
        """
        arguments = shlex.split(arg)
        instances = 0
        objects = storage.all()
        if len(arguments) > 0:
            if arguments[0] in self.__classes:
                for obj in objects.values():
                    if arguments[0] == obj.__class__.__name__:
                        instances += 1
                print(instances)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
