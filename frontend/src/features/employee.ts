// Exemplo de feature slice
export interface Employee {
  id: number;
  name: string;
  department: string;
  position: string;
  status: string;
}

export interface EmployeeState {
  employees: Employee[];
  loading: boolean;
}

// ...reducers/actions para employees
