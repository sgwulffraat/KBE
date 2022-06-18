from parapy.core import Base, Part, Input


class Foo(Base):
    parsing_color = Input('purple')
    no_parsing_color = Input('red')

    @Part
    def parsing(self):
        return Base(color=self.parsing_color)

    @Part(parse=False)
    def no_parsing(self):
        return Base(color=self.no_parsing_color)


foo = Foo()

# the default behaviour of a Part is that it will evaluate the Inputs of the
# child lazy:
parsing = foo.parsing
assert not foo.get_slot_status('parsing_color')  # parsing color not evaluated
# requesting the color on parsing:
print(f"parsing has the color {parsing.color}")
assert foo.get_slot_status('parsing_color')  # now it is evaluated

# before no_parsing is calculated:
assert not foo.get_slot_status('no_parsing_color')  # not yet evaluated

no_parsing = foo.no_parsing
# requesting the object will immediately evaluate no_parsing_color
assert foo.get_slot_status('no_parsing_color')  # it is evaluated

# Both instances will receive 'foo' as their parent:
print(f"parent parsing: {foo.parsing.parent}, "
      f"parent no_parsing: {foo.no_parsing.parent}, "
      f"foo: {foo}")


class Bar(Base):
    @Part(parse=False)
    def quz(self):
        # not having a Part allows you to use any Python syntax you like,
        # at the cost of evaluating all the passed Inputs as soon as
        # quz is requested.
        # Every ParaPy object that is returned will become a child
        return [Base(color='black'), Base(color='white')]


bar = Bar()
# both Base instances have received a parent
print(f"parent quz[0]: {bar.quz[0].parent}, "
      f"parent quz[1]: {bar.quz[1].parent}, "
      f"bar: {bar}")