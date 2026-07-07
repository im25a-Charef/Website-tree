
import sys
import pygame

website_routes = {
    "/": {
        "name": "Homepage",
        "description": "Main landing page",
        "side_urls": {
            "about": {
                "name": "About Us",
                "description": "Company history and team",
                "side_urls": {
                    "team": {
                        "name": "Our Team",
                        "description": "Bio pages for staff",
                        "side_urls": {},
                    },
                    "careers": {
                        "name": "Careers",
                        "description": "Job openings",
                        "side_urls": {},
                    },
                },
            },
            "shop": {
                "name": "E-Commerce Store",
                "description": "Main product catalog",
                "side_urls": {
                    "products": {
                        "name": "Product Details",
                        "description": "Dynamic product pages",
                        "side_urls": {},
                    },
                    "cart": {
                        "name": "Shopping Cart",
                        "description": "User's selected items",
                        "side_urls": {},
                    },
                },
            },
            "contact": {
                "name": "Contact Page",
                "description": "Contact form and map",
                "side_urls": {},
            },
        },
    }
}

pygame.init()

sib_offset = 100


class Leaf:

    def __init__(
            self,
            x,
            y,
            width,
            height,
            color,
            name,
            sibling_of=None,
            children_of= None,
            sibling_l=None,
            offset=sib_offset
    ):
        if children_of is None:
            children_of = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name
        self.sibling_of = sibling_of
        self.children_of = children_of
        self.sibling_l = sibling_l
        self.offset = offset

        if sibling_of:
            self.sibling_of.sibling_l = self
            print(sibling_of.sibling_l.name)


leaves = []

leaves.append(Leaf(50, 200, 20, 20, (255, 0, 0), "leaf0"))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Tree Map")

clock = pygame.time.Clock()


def main():
    global sib_offset
    running = True

    zoom_factor = 1.0
    offset_x = 0
    offset_y = 0
    pan_speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_m:
                    if len(leaves) > 0:
                        parent_sibling = leaves[-1]
                        new_leaf = Leaf(
                            x=0,
                            y=parent_sibling.y,
                            width=20,
                            height=20,
                            color=GREEN,
                            name=f"leaf{len(leaves)}",
                            sibling_of=parent_sibling,
                        )
                        leaves.append(new_leaf)

        keys = pygame.key.get_pressed()


        if keys[pygame.K_UP]:
            sib_offset += 2
        if keys[pygame.K_DOWN]:
            sib_offset = max(10, sib_offset - 2)


        if keys[pygame.K_COMMA]:
            zoom_factor = max(0.1, zoom_factor - 0.02)
        if keys[pygame.K_PERIOD]:
            zoom_factor = min(5.0, zoom_factor + 0.02)


        if keys[pygame.K_a]:
            offset_x += pan_speed
        if keys[pygame.K_d]:
            offset_x -= pan_speed
        if keys[pygame.K_w]:
            offset_y += pan_speed
        if keys[pygame.K_s]:
            offset_y -= pan_speed


        screen.fill(BLACK)

        for i, leaf_node in enumerate(leaves):
            if leaf_node.sibling_of:
                leaf_node.x = (
                        leaf_node.sibling_of.x + leaf_node.width + sib_offset
                )

                start_x = (leaf_node.sibling_of.x + leaf_node.width) * zoom_factor + offset_x
                start_y = (leaf_node.sibling_of.y + leaf_node.height / 2) * zoom_factor + offset_y
                end_x = leaf_node.x * zoom_factor + offset_x
                end_y = (leaf_node.y + leaf_node.height / 2) * zoom_factor + offset_y

                pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), int(2 * zoom_factor) or 1)

            draw_x = leaf_node.x * zoom_factor + offset_x
            draw_y = leaf_node.y * zoom_factor + offset_y
            draw_w = leaf_node.width * zoom_factor
            draw_h = leaf_node.height * zoom_factor

            pygame.draw.rect(
                screen,
                leaf_node.color,
                (draw_x, draw_y, draw_w, draw_h),
            )
        #elif i.children_of != []:


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print(website_routes)
    main()