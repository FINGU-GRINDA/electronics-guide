// src/shadcn-ui/Button.tsx
import React from "react";
import { cn } from "../utils/cn"; // Utility to combine class names

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

const Button: React.FC<ButtonProps> = ({ className, ...props }) => {
  return (
    <button
      className={cn(
        "px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none",
        className
      )}
      {...props}
    />
  );
};

export default Button;
