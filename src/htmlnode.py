class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        if not isinstance(self.props, dict):
            raise ValueError("properties must be entered as a dictonary object")
        str_convert = list(map(lambda item: f" {item}=\"{self.props[item]}\"", self.props.keys()))
        return "".join(str_convert)
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        print(f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if (value == "" or value is None) and tag != "img":
            raise ValueError("value must be defined")
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag == "" or tag is None:
            raise ValueError("ParentNode must contain a tag")
        if children == "" or children is None:
            raise ValueError("ParentNode must contain at least one child")
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == "" or self.tag is None:
            raise ValueError("ParentNode must contain a tag")
        if self.children == "" or self.children is None:
            raise ValueError("ParentNode must contain at least one child")       
        completed_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            completed_string += child.to_html()
            
        completed_string += f"</{self.tag}>"
        return completed_string
    


