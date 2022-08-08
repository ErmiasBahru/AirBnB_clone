#!/usr/bin/python3
"""
This is a module for HBNBCommand class.
"""
import shlex
import cmd
import models
import helper_function as hf
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Class representing the HBNBcommand class"""
    prompt = '(hbnb) '
    valid_classes = {'BaseModel': BaseModel,
                     'User': User,
                     'State': State,
                     'City': City,
                     'Amenity': Amenity,
                     'Place': Place,
                     'Review': Review}

    valid_class_strings = {'BaseModel': 'BaseModel',
                           'User': 'User',
                           'State': 'State',
                           'City': 'City',
                           'Amenity': 'Amenity',
                           'Place': 'Place',
                           'Review': 'Review'}

    valid_commands = {'all': hf.all,
                      'count': hf.count,
                      'show': hf.show,
                      'destroy': hf.destroy}

    objects_dict = models.storage._FileStorage__objects

    def default(self, arg):
        args = arg.split(".")
        try:
            class_name = HBNBCommand.valid_class_strings[args[0]]
            arg = args[1][args[1].find("(")+1:args[1].find(")")]
            command = args[1][:args[1].find("(")]
            command = HBNBCommand.valid_commands[command]
            command(class_name, arg)
        except:
            return(cmd.Cmd.default(self, arg))

    def do_quit(self, s):
        """A method that allows users to quit."""
        return True

    def help_quit(self):
        """A method that allows users to get documentation on quit."""
        print("Quit command to exit the program")

    def emptyline(self):
        """A method that overwrites the default when no command is given."""
        pass

    do_EOF = do_quit
    help_EOF = help_quit

    def do_create(self, arg):
        """A method that creates an instance of a class."""
        if not arg:
            print("** class name missing **")
        elif arg in self.valid_classes:
            x = self.valid_classes[arg]
            y = x()
            y.save()
            print(y.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """A method that allows users to get documentation on create."""
        print("A command that creates an instance of a class")

    def do_show(self, arg):
        """A method that shows instance information."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] in self.valid_classes:
            if len(args) < 2:
                print("** instance id missing **")
            elif "{}.{}".format(args[0], args[1]) in HBNBCommand.objects_dict:
                print(HBNBCommand.objects_dict["{}.{}".format(args[0],
                                                              args[1])])
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def help_show(self):
        """A method that allows users to get documentation on show."""
        print("A command that shows the information of an instance")

    def do_destroy(self, arg):
        """
        A method that deletes an instance based on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] in self.valid_classes:
            if len(args) != 2:
                print("** instance id missing **")
            elif "{}.{}".format(args[0], args[1]) in HBNBCommand.objects_dict:
                del(HBNBCommand.objects_dict["{}.{}".format(args[0], args[1])])
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")
        models.storage.save()

    def help_destroy(self):
        """A method that allows users to get documentation on destroy."""
        print(("A command that destroys an instance based") +
              (" on the class name and id"))

    def do_all(self, arg):
        """
        A method that prints all string representation of amodels.storage.
        FileStorage__objects[key]))ll instances based
        on the class name or not.
        """
        args = shlex.split(arg)
        ret_list = []

        if not arg:
            for class_name_key in self.valid_classes:
                for key in HBNBCommand.objects_dict:
                    if class_name_key in key:
                        ret_list.append(str(HBNBCommand.objects_dict[key]))
            print(ret_list)
        else:
            if args[0] in self.valid_classes:
                for key in HBNBCommand.objects_dict:
                    if args[0] in key:
                        ret_list.append(str(HBNBCommand.objects_dict[key]))
                print(ret_list)
            else:
                print("** class doesn't exist **")

    def help_all(self):
        """A method that allows users to get documentation on all."""
        print(("A command that prints all string representation of all ") +
              ("instances"))

    def do_update(self, arg):
        """A method that updates an instance based on the class name and id
        by adding or updating attribute."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            # return
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
            return
        else:
            key = "{}.{}".format(args[0], args[1])
            try:
                instance = HBNBCommand.objects_dict[key]
            except:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            else:
                if len(args) < 4:
                    print("** value missing **")
                    return
                else:
                    try:
                        type_ = type(getattr(instance, args[2]))
                        try:
                            setattr(instance, args[2], type_(args[3]))
                        except:
                            print("You can't cast to type: {}".format(type_))
                    except:
                        setattr(instance, args[2], str(args[3]))

    def help_update(self):
        """A command that updates instances. Usage: update <class name> """
        print(("Usage: update <class name> <id> <attribute name> ") +
              ("<attribute value>"))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
