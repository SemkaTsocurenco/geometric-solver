# main.py
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constraint_solver import ConstraintSolver
import math

class GeometrySolver:
    def __init__(self):
        self.points = {}
        self.lines = []
        self.next_point_id = 0
        self.selected_points_for_line = []
        self.selected_line = None
        self.selected_lines = []
        self.add_point_mode = True
        self.free_line_mode = False
        self.constraint_mode = False
        self.dragging_point_id = None
        self.dragging_line_id = None
        self.mouse_pressed = False
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.single_click = False
        self.single_click_x = None
        self.single_click_y = None
        self.drag_threshold = 0.1
        self.last_free_line_point = None
        self.root = tk.Tk()
        self.root.title("Geometry Solver")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.button_create_line = tk.Button(self.control_frame, text='Create Line', command=self.on_create_line_button_clicked)
        self.button_delete = tk.Button(self.control_frame, text='Delete', command=self.on_delete_clicked)
        self.button_free_line = tk.Button(self.control_frame, text='Free Line Mode', command=self.on_free_line_mode_clicked)
        self.button_set_dist = tk.Button(self.control_frame, text='Set Distance', command=self.on_set_distance_button_clicked)
        self.button_constraint_mode = tk.Button(self.control_frame, text='Constraint Mode', command=self.on_constraint_mode_clicked)
        self.button_clear = tk.Button(self.control_frame, text='Clear Selections', command=self.on_clear_selections_clicked)
        self.button_constraint_mode.pack(pady=5)
        self.button_clear.pack(pady=5)
        self.constraint_buttons = []
        btn_dist = tk.Button(self.control_frame, text="Set Distance (C)", command=self.on_constraint_set_distance)
        self.constraint_buttons.append(btn_dist)
        btn_perp = tk.Button(self.control_frame, text="Make Perpendicular", command=self.on_constraint_perpendicular)
        self.constraint_buttons.append(btn_perp)
        btn_par = tk.Button(self.control_frame, text="Make Parallel", command=self.on_constraint_parallel)
        self.constraint_buttons.append(btn_par)
        btn_point_on_line = tk.Button(self.control_frame, text="Point on Line", command=self.on_constraint_point_on_line)
        self.constraint_buttons.append(btn_point_on_line)
        btn_angle = tk.Button(self.control_frame, text="Set Angle", command=self.on_constraint_angle)
        self.constraint_buttons.append(btn_angle)
        btn_stationary = tk.Button(self.control_frame, text="Make Stationary", command=self.on_constraint_stationary)
        self.constraint_buttons.append(btn_stationary)
        btn_hor = tk.Button(self.control_frame, text="Make Horizontal", command=self.on_constraint_horizontal)
        self.constraint_buttons.append(btn_hor)
        btn_ver = tk.Button(self.control_frame, text="Make Vertical", command=self.on_constraint_vertical)
        self.constraint_buttons.append(btn_ver)
        self.constraints_label = tk.Label(self.control_frame, text="Constraints:")
        self.constraints_label.pack(pady=5)
        self.constraints_text = scrolledtext.ScrolledText(self.control_frame, height=15, width=40)
        self.constraints_text.pack(pady=5)
        self.plot_frame = tk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.cid_button_press = self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.cid_motion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_button_release = self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.constraint_solver = ConstraintSolver(self.points)
        self.constraint_solver.set_confirmation_callback(self.confirm_deletion)
        self.show_standard_buttons()
        self.redraw()
        self.root.after(50, self.update_continuously)

    def update_continuously(self):
        self.constraint_solver.set_lines_reference(self.lines)
        self.constraint_solver.solve_constraints()
        self.redraw()
        self.root.after(50, self.update_continuously)

    def confirm_deletion(self, message):
        return messagebox.askyesno("Confirm deletion", message)

    def add_point(self, x, y):
        point_id = self.next_point_id
        self.points[point_id] = (x, y)
        self.next_point_id += 1
        return point_id

    def move_point(self, point_id, new_x, new_y):
        if point_id in self.points:
            if not self.constraint_solver.is_stationary(point_id):
                self.points[point_id] = (new_x, new_y)

    def add_line(self, point1_id, point2_id):
        if point1_id in self.points and point2_id in self.points and point1_id != point2_id:
            self.lines.append((point1_id, point2_id))

    def move_line(self, line_index, dx, dy):
        if line_index is None or line_index < 0 or line_index >= len(self.lines):
            return
        p1_id, p2_id = self.lines[line_index]
        if p1_id in self.points and not self.constraint_solver.is_stationary(p1_id):
            x1, y1 = self.points[p1_id]
            self.points[p1_id] = (x1+dx, y1+dy)
        if p2_id in self.points and not self.constraint_solver.is_stationary(p2_id):
            x2, y2 = self.points[p2_id]
            self.points[p2_id] = (x2+dx, y2+dy)

    def redraw(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        for point_id, (x, y) in self.points.items():
            color = 'red' if point_id in self.selected_points_for_line else 'blue'
            self.ax.scatter(x, y, color=color)
            self.ax.text(x, y+0.2, f"ID:{point_id} ({x:.1f},{y:.1f})", color='green', fontsize=8, ha='center')
        new_lines = []
        for i, (p1_id, p2_id) in enumerate(self.lines):
            if p1_id in self.points and p2_id in self.points:
                x1, y1 = self.points[p1_id]
                x2, y2 = self.points[p2_id]
                line_color = 'red' if i in self.selected_lines else 'black'
                self.ax.plot([x1, x2], [y1, y2], color=line_color)
                mid_x = (x1 + x2)/2.0
                mid_y = (y1 + y2)/2.0
                length = math.hypot(x2 - x1, y2 - y1)
                self.ax.text(mid_x, mid_y+0.3, f"Line {i}: {length:.2f}", color='purple', fontsize=8, ha='center')
                new_lines.append((p1_id, p2_id))
        self.lines = new_lines
        mode_str = ("Constraint Mode" if self.constraint_mode else ("Free Line Mode" if self.free_line_mode else ("Add Point Mode" if self.add_point_mode else "Select/Move Mode")))
        self.ax.set_title(mode_str)
        self.canvas.draw_idle()
        self.update_constraints_text()

    def update_constraints_text(self):
        pos = self.constraints_text.yview()
        self.constraints_text.delete("1.0", tk.END)
        constraints = self.constraint_solver.get_constraints_info()
        for idx, c in enumerate(constraints, start=1):
            ctype = c["type"]
            objs = c["objects"]
            val = c.get("value", None)
            self.constraints_text.insert(tk.END, f"{idx}. {ctype}\n")
            if ctype == "distance":
                p1,p2 = objs
                x1,y1=self.points.get(p1,(0,0))
                x2,y2=self.points.get(p2,(0,0))
                self.constraints_text.insert(tk.END, f"   P1: {p1} ({x1:.2f},{y1:.2f})\n")
                self.constraints_text.insert(tk.END, f"   P2: {p2} ({x2:.2f},{y2:.2f})\n")
                self.constraints_text.insert(tk.END, f"   Distance: {val}\n")
            else:
                self.constraints_text.insert(tk.END, f"   Objects: {objs}\n")
                if val is not None:
                    self.constraints_text.insert(tk.END, f"   Value: {val}\n")
            self.constraints_text.insert(tk.END, "\n")
        self.constraints_text.yview_moveto(pos[0])

    def find_nearest_point(self, x, y, threshold=1.0):
        if not self.points:
            return None
        distances = {pid: np.hypot(x - px, y - py) for pid, (px, py) in self.points.items()}
        nearest_point = min(distances, key=distances.get)
        if distances[nearest_point] < threshold:
            return nearest_point
        return None

    def find_nearest_line(self, x, y, threshold=1.0):
        if not self.lines:
            return None
        def point_to_segment_dist(px, py, x1, y1, x2, y2):
            A = np.array([x1, y1])
            B = np.array([x2, y2])
            P = np.array([px, py])
            AB = B - A
            AP = P - A
            denom = np.dot(AB, AB)
            if denom == 0:
                return np.linalg.norm(P - A)
            t = np.dot(AP, AB)/denom
            t = max(0, min(1, t))
            closest = A + t * AB
            return np.linalg.norm(P - closest)
        line_distances = {}
        for i, (p1_id, p2_id) in enumerate(self.lines):
            if p1_id not in self.points or p2_id not in self.points:
                continue
            x1, y1 = self.points[p1_id]
            x2, y2 = self.points[p2_id]
            dist = point_to_segment_dist(x, y, x1, y1, x2, y2)
            line_distances[i] = dist
        if not line_distances:
            return None
        nearest_line = min(line_distances, key=line_distances.get)
        if line_distances[nearest_line] < threshold:
            return nearest_line
        return None

    def clear_selection(self):
        self.selected_points_for_line = []
        self.selected_line = None

    def toggle_point_selection(self, point_id):
        if point_id in self.selected_points_for_line:
            self.selected_points_for_line.remove(point_id)
        else:
            if len(self.selected_points_for_line) >= 2:
                self.selected_points_for_line = []
            self.selected_points_for_line.append(point_id)

    def on_button_press(self, event):
        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:
            self.mouse_pressed = True
            self.last_mouse_x = event.xdata
            self.last_mouse_y = event.ydata

            if self.constraint_mode:
                p = self.find_nearest_point(event.xdata, event.ydata)
                l = None if p is not None else self.find_nearest_line(event.xdata, event.ydata)
                if p is None and l is None:
                    self.clear_selection()
                    self.selected_lines = []
                    self.redraw()
                    return
                if p is not None:
                    if len(self.selected_lines) == 2:
                        messagebox.showerror("Error", "Invalid selection")
                        return
                    if len(self.selected_points_for_line) < 2:
                        if p not in self.selected_points_for_line:
                            self.selected_points_for_line.append(p)
                    else:
                        messagebox.showerror("Error", "2 points already selected.")
                else:
                    if len(self.selected_points_for_line) == 2:
                        messagebox.showerror("Error", "2 points selected.")
                        return
                    if l not in self.selected_lines:
                        if len(self.selected_lines) < 2:
                            self.selected_lines.append(l)
                        else:
                            messagebox.showerror("Error", "2 lines already selected.")
                self.redraw()
                return

            if self.free_line_mode:
                p = self.find_nearest_point(event.xdata, event.ydata)
                if p is not None:
                    if self.last_free_line_point is None:
                        self.last_free_line_point = p
                    else:
                        if p != self.last_free_line_point:
                            self.add_line(self.last_free_line_point, p)
                            self.last_free_line_point = p
                    self.redraw()
                else:
                    p_id = self.add_point(event.xdata, event.ydata)
                    if self.last_free_line_point is not None:
                        self.add_line(self.last_free_line_point, p_id)
                    self.last_free_line_point = p_id
                    self.redraw()
                return

            p = self.find_nearest_point(event.xdata, event.ydata)
            l = None if p is not None else self.find_nearest_line(event.xdata, event.ydata)

            if self.add_point_mode:
                self.single_click = True
                self.single_click_x = event.xdata
                self.single_click_y = event.ydata
                if p is not None:
                    self.toggle_point_selection(p)
                    if len(self.selected_points_for_line) == 1 and self.selected_points_for_line[0] == p:
                        self.dragging_point_id = p
                    else:
                        self.dragging_point_id = None
                    self.selected_line = None
                    self.redraw()
                elif l is not None:
                    self.clear_selection()
                    self.selected_line = l
                    self.dragging_line_id = l
                    self.redraw()
                else:
                    self.clear_selection()
                    self.redraw()
            else:
                self.single_click = True
                self.single_click_x = event.xdata
                self.single_click_y = event.ydata
                if p is not None:
                    self.toggle_point_selection(p)
                    if len(self.selected_points_for_line) == 1 and self.selected_points_for_line[0] == p:
                        self.dragging_point_id = p
                    else:
                        self.dragging_point_id = None
                    self.selected_line = None
                    self.redraw()
                elif l is not None:
                    self.clear_selection()
                    self.selected_line = l
                    self.dragging_line_id = l
                    self.redraw()
                else:
                    self.clear_selection()
                    self.redraw()

        elif event.button == 3 and not self.constraint_mode:
            if len(self.selected_points_for_line) == 2:
                p1, p2 = self.selected_points_for_line
                self.add_line(p1, p2)
                self.clear_selection()
                self.redraw()

    def on_motion(self, event):
        if event.xdata is None or event.ydata is None:
            return
        if self.free_line_mode or self.constraint_mode:
            return
        if self.mouse_pressed and event.button == 1 and event.xdata is not None and event.ydata is not None:
            dist = np.hypot(event.xdata - self.single_click_x, event.ydata - self.single_click_y)
            if dist > self.drag_threshold:
                self.single_click = False
            if not self.free_line_mode:
                if self.dragging_point_id is not None:
                    self.move_point(self.dragging_point_id, event.xdata, event.ydata)
                elif self.dragging_line_id is not None:
                    dx = event.xdata - self.last_mouse_x
                    dy = event.ydata - self.last_mouse_y
                    self.move_line(self.dragging_line_id, dx, dy)
                    self.last_mouse_x = event.xdata
                    self.last_mouse_y = event.ydata

    def on_button_release(self, event):
        if event.button == 1:
            self.mouse_pressed = False
            if self.free_line_mode or self.constraint_mode:
                return
            if self.add_point_mode:
                if self.single_click and self.single_click_x is not None and self.single_click_y is not None:
                    p = self.find_nearest_point(self.single_click_x, self.single_click_y)
                    l = None if p is not None else self.find_nearest_line(self.single_click_x, self.single_click_y)
                    if p is None and l is None:
                        new_p = self.add_point(self.single_click_x, self.single_click_y)
            self.dragging_point_id = None
            self.dragging_line_id = None
            self.single_click = False
            self.single_click_x = None
            self.single_click_y = None

    def show_standard_buttons(self):
        self.button_create_line.pack(pady=5)
        self.button_delete.pack(pady=5)
        self.button_free_line.pack(pady=5)
        self.button_set_dist.pack(pady=5)
        for b in self.constraint_buttons:
            b.pack_forget()

    def show_constraint_buttons(self):
        self.button_create_line.pack_forget()
        self.button_delete.pack_forget()
        self.button_free_line.pack_forget()
        self.button_set_dist.pack_forget()
        for b in self.constraint_buttons:
            b.pack(pady=5)

    def on_constraint_mode_clicked(self):
        self.constraint_mode = not self.constraint_mode
        if self.constraint_mode:
            self.show_constraint_buttons()
        else:
            self.show_standard_buttons()
        self.clear_selection()
        self.selected_lines = []
        self.redraw()

    def on_create_line_button_clicked(self):
        if not self.constraint_mode and len(self.selected_points_for_line) == 2:
            p1, p2 = self.selected_points_for_line
            self.add_line(p1, p2)
            self.clear_selection()
            self.redraw()

    def on_clear_selections_clicked(self):
        self.clear_selection()
        self.selected_lines = []
        self.redraw()

    def on_delete_clicked(self):
        if self.constraint_mode:
            return
        self.delete_selected_objects()

    def on_free_line_mode_clicked(self):
        if self.constraint_mode:
            return
        if self.free_line_mode:
            self.free_line_mode = False
            self.last_free_line_point = None
        else:
            self.free_line_mode = True
            self.last_free_line_point = None
            self.clear_selection()
        self.redraw()

    def on_set_distance_button_clicked(self):
        if self.constraint_mode:
            return
        if len(self.selected_points_for_line) == 2:
            self.show_distance_input_dialog()

    def show_distance_input_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Distance")
        tk.Label(dialog, text="Enter the desired distance:").pack(pady=5)
        distance_entry = tk.Entry(dialog)
        distance_entry.pack(pady=5)
        def confirm():
            try:
                dist = float(distance_entry.get())
                if dist >= 0.0:
                    p1, p2 = self.selected_points_for_line
                    self.constraint_solver.add_distance_constraint(p1, p2, dist)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Distance must be non-negative.")
            except ValueError:
                messagebox.showerror("Error", "Invalid distance value.")
        confirm_btn = tk.Button(dialog, text="OK", command=confirm)
        confirm_btn.pack(pady=5)
        dialog.grab_set()
        dialog.focus_set()

    def on_constraint_set_distance(self):
        if len(self.selected_points_for_line) == 2 and len(self.selected_lines) == 0:
            p1, p2 = self.selected_points_for_line
            dialog = tk.Toplevel(self.root)
            dialog.title("Set Distance (Constraint)")
            tk.Label(dialog, text="Enter the desired distance:").pack(pady=5)
            distance_entry = tk.Entry(dialog)
            distance_entry.pack(pady=5)
            def confirm():
                try:
                    dist = float(distance_entry.get())
                    if dist < 0:
                        raise ValueError
                    if not self.constraint_solver.add_distance_constraint(p1, p2, dist):
                        messagebox.showerror("Error", "Failed")
                    dialog.destroy()
                except:
                    messagebox.showerror("Error", "Invalid distance.")
            tk.Button(dialog, text="OK", command=confirm).pack(pady=5)
            dialog.grab_set()
            dialog.focus_set()
        else:
            messagebox.showerror("Error", "Select exactly two points.")

    def on_constraint_perpendicular(self):
        if len(self.selected_lines) == 2 and len(self.selected_points_for_line) == 0:
            l1, l2 = self.selected_lines
            if not self.constraint_solver.add_perpendicular_constraint(l1, l2):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select exactly two lines.")

    def on_constraint_parallel(self):
        if len(self.selected_lines) == 2 and len(self.selected_points_for_line) == 0:
            l1, l2 = self.selected_lines
            if not self.constraint_solver.add_parallel_constraint(l1, l2):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select exactly two lines.")

    def on_constraint_point_on_line(self):
        if len(self.selected_points_for_line) == 1 and len(self.selected_lines) == 1:
            p = self.selected_points_for_line[0]
            l = self.selected_lines[0]
            if not self.constraint_solver.add_point_on_line_constraint(p, l):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select one point and one line.")

    def on_constraint_angle(self):
        if len(self.selected_lines) == 2 and len(self.selected_points_for_line) == 0:
            l1, l2 = self.selected_lines
            dialog = tk.Toplevel(self.root)
            dialog.title("Set Angle")
            tk.Label(dialog, text="Enter angle in degrees:").pack(pady=5)
            angle_entry = tk.Entry(dialog)
            angle_entry.pack(pady=5)
            def confirm():
                try:
                    angle = float(angle_entry.get())
                    if not self.constraint_solver.add_angle_constraint(l1, l2, angle):
                        messagebox.showerror("Error", "Failed")
                    dialog.destroy()
                except:
                    messagebox.showerror("Error", "Invalid angle.")
            tk.Button(dialog, text="OK", command=confirm).pack(pady=5)
            dialog.grab_set()
            dialog.focus_set()
        else:
            messagebox.showerror("Error", "Select two lines.")

    def on_constraint_stationary(self):
        if len(self.selected_points_for_line) == 1 and len(self.selected_lines) == 0:
            p = self.selected_points_for_line[0]
            if not self.constraint_solver.add_stationary_constraint(p):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select exactly one point.")

    def on_constraint_horizontal(self):
        if len(self.selected_lines) == 1 and len(self.selected_points_for_line) == 0:
            l = self.selected_lines[0]
            if not self.constraint_solver.add_horizontal_constraint(l):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select exactly one line.")

    def on_constraint_vertical(self):
        if len(self.selected_lines) == 1 and len(self.selected_points_for_line) == 0:
            l = self.selected_lines[0]
            if not self.constraint_solver.add_vertical_constraint(l):
                messagebox.showerror("Error", "Failed")
        else:
            messagebox.showerror("Error", "Select exactly one line.")

    def delete_selected_objects(self):
        if self.selected_line is not None:
            line_index = self.selected_line
            if line_index < len(self.lines):
                p1_id, p2_id = self.lines[line_index]
                if self.constraint_solver.on_point_delete(p1_id) and self.constraint_solver.on_point_delete(p2_id):
                    del self.lines[line_index]
            self.clear_selection()
            self.selected_lines = []
            self.redraw()
            return
        if len(self.selected_points_for_line) > 0:
            for pid in self.selected_points_for_line:
                if not self.constraint_solver.on_point_delete(pid):
                    return
            for pid in self.selected_points_for_line:
                if pid in self.points:
                    del self.points[pid]
            new_lines = []
            for (p1, p2) in self.lines:
                if p1 in self.points and p2 in self.points:
                    new_lines.append((p1, p2))
            self.lines = new_lines
            self.clear_selection()
            self.selected_lines = []
            self.redraw()

    def show(self):
        self.root.mainloop()

if __name__ == '__main__':
    solver = GeometrySolver()
    solver.show()
