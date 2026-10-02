#!/usr/bin/python3
"""Command interpreter for the AirBnB clone project."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""

    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """Creates a new instance of a class with given parameters
        Usage: create <Class name> <param 1> <param 2> ...
        Param syntax: <key name>=<value>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create the new instance
        new_instance = HBNBCommand.classes[class_name]()

        # Process parameters
        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)

            # String value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]                 # remove quotes
                value = value.replace("_", " ")     # underscores → spaces
                value = value.replace('\\"', '"')   # unescape quotes
            # Float value
            elif "." in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            # Integer value
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)    def do_create(self, arg):
        """Create a new instance, save it and print the id."""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        obj = self.classes[arg]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Print the string representation of an instance."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Print all string representation of all instances."""
        args = arg.split()
        obj_list = []
        if len(args) == 0:
            for obj in storage.all().values():
                obj_list.append(str(obj))
        else:
            if args[0] not in self.classes:
                print("** class doesn't exist **")
                return
            for key, obj in storage.all().items():
                if key.startswith(args[0] + "."):
                    obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Update an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]

        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]
        else:
            try:
                if '.' in attr_value:
                    attr_value = float(attr_value)
                else:
                    attr_value = int(attr_value)
            except ValueError:
                pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
