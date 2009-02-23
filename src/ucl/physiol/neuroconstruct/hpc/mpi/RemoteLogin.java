/**
 *  neuroConstruct
 *  Software for developing large scale 3D networks of biologically realistic neurons
 *
 *  Copyright (c) 2009 Padraig Gleeson
 *  UCL Department of Neuroscience, Physiology and Pharmacology
 *
 *  Development of this software was made possible with funding from the
 *  Medical Research Council and the Wellcome Trust
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

package ucl.physiol.neuroconstruct.hpc.mpi;


/**
 * Support for interacting with MPI platform
 *
 * @author Padraig Gleeson
 *
 */
public class RemoteLogin
{
    private String hostname = null;

    private String workDir = null;

    public RemoteLogin()
    {

    }

    public RemoteLogin(String hostname, String workDir)
    {
        this.hostname = hostname;
        this.workDir = workDir;
    }


    public String getHostname()
    {
        return hostname;
    }

    public void setHostname(String hostname)
    {
        this.hostname = hostname;
    }

    public String getWorkDir()
    {
        return workDir;
    }

    public void setWorkDir(String workDir)
    {
        this.workDir = workDir;
    }


    @Override
    public Object clone()
    {
        RemoteLogin rl2 = new RemoteLogin(new String(hostname), new String(workDir));
        return rl2;

    }


    @Override
    public boolean equals(Object obj)
    {
        if (obj == null)
        {
            return false;
        }
        if (getClass() != obj.getClass())
        {
            return false;
        }
        final RemoteLogin other = (RemoteLogin) obj;
        if ((this.hostname == null) ? (other.hostname != null) : !this.hostname.equals(other.hostname))
        {
            return false;
        }
        if ((this.workDir == null) ? (other.workDir != null) : !this.workDir.equals(other.workDir))
        {
            return false;
        }
        return true;
    }

    @Override
    public int hashCode()
    {
        int hash = 5;
        hash = 83 * hash + (this.hostname != null ? this.hostname.hashCode() : 0);
        hash = 83 * hash + (this.workDir != null ? this.workDir.hashCode() : 0);
        return hash;
    }
    


}
